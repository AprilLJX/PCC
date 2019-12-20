import sqlite3
import json

from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route('/signup',methods=["GET","POST"])
def signup():
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()


    data = (request.get_data(as_text=True))
    print(type(data))
    data = json.loads(data)
    # data = json.loads(request.get_data(as_text=True))
    phone = data.get('phone')
    nickname = data.get('nickname')
    password = data.get('password')
    
    SQL = "SELECT userid from usertable where phone = '%s' "%phone
    user = c.execute(SQL)
    
    user = list(user)
    phone_exist = True if len(user) else False;

    res = {}
    if phone_exist:
        res["status"] = '0'
    else:
        c.execute("INSERT INTO usertable(nickname,phone,password) VALUES (?,?,?)",(nickname,phone,password))
        conn.commit()
        res["status"] = '1'

    conn.close()
    res = json.dumps(res)

    return res

@app.route('/login',methods=["GET","POST"])
def login():

    data = json.loads(request.get_data(as_text=True))
    phone = data.get('phone')
    password = data.get('password')
    
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    cursor = c.execute("SELECT userid,phone,password from usertable where phone = '{}'".format(phone))

    cursor = list(cursor)
    
    res = {}
    if len(cursor):
        if str(cursor[0][1]) == phone and str(cursor[0][2]) == password:
            res['status'] = '1'
            res['uid'] = cursor[0][0]
        else:
            res['status'] = '0'
    else:
        res['status'] = '0'

    conn.close()

    return res

@app.route('/startcarpool',methods=["GET","POST"])
def startCar():
    data = json.loads(request.get_data(as_text=True))
    startpoint = data.get('startpoint')
    endpoint = data.get('endpoint')
    startdate = data.get('startdate')
    starttime = data.get('starttime')
    maxnum = data.get('num')
    price = data.get('price')
    userid_1 = data.get('userid_1')
    remark = data.get('remark')

    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    c.execute("INSERT INTO cartable(startpoint,endpoint,startdate,starttime,maxnum,price,userid_1,remark) "
              "VALUES (?,?,?,?,?,?,?)", (startpoint,endpoint,startdate,starttime,maxnum,price,userid_1,remark))
    carid = c.lastrowid
    conn.commit()
    conn.close()

    res = {}
    res['carid'] = carid

    return res

@app.route('/joincarpool',methods=["GET","POST"])
def joinCar():
    data = json.loads(request.get_data(as_text=True))
    carid = data.get('carid')
    userid = data.get('userid')

    useradd = "userid_"
    currentnum = 0

    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    cursor = c.execute("SELECT currentnum FROM cartable WHERE carid = '{}'".format(carid))
    cursor = list(cursor)

    if len(cursor):
        currentnum = cursor[0][0] + 1
        useradd += str(currentnum)

    conn.close()

    res = {}
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    c.execute("UPDATE cartable SET currentnum = {},{}={} WHERE carid = '{}'".format(currentnum,useradd,userid,carid))
    conn.commit()
    conn.close()

    res["status"] = 1
    return res

@app.route('/exitcarpool',methods=["GET","POST"])
def exitCar():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get('userid')
    carid = data.get('carid')

    res = {}
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    cursor = list(c.execute("SELECT userid_1,userid_2,userid_3,userid_4,currentnum FROM cartable WHERE carid = {}".format(carid)))
    if str(cursor[0][0]) == userid:
        # TODO 直接删除是否太暴力了
        c.execute("DELETE FROM cartable WHERE carid = {}".format(carid))
        res["status"] = "删除成功"
    elif str(cursor[0][1]) == userid:
        c.execute("UPDATE cartable SET userid_2 = NULL,currentnum = {}  WHERE carid = {}".format(cursor[0][4]-1,carid))
        res["status"] = "退出拼车成功"
    elif str(cursor[0][2]) == userid:
        c.execute("UPDATE cartable SET userid_3 = NULL,currentnum = {}  WHERE carid = {}".format(cursor[0][4]-1,carid))
        res["status"] = "退出拼车成功"
    elif str(cursor[0][3]) == userid:
        c.execute("UPDATE cartable SET userid_4 = NULL,currentnum = {}  WHERE carid = {}".format(cursor[0][4]-1,carid))
        res["status"] = "退出拼车成功"
    else:
        res["status"] = "失败，没有权限"

    conn.commit()
    conn.close()

    return res


@app.route('/showusermessage',methods=["GET","POST"])
def showUserMes():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get("userid")

    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM usertable WHERE userid = {}".format(userid))
    cursor = list(cursor)

    res = {}

    for row in cursor:
        res["userid"] = row[0]
        res["nickname"] = row[1]
        res["phone"] = row[2]
        res["headImg"] = row[3]
        res["gender"] = row[4]
        res["infor"] = row[5]

    return res

@app.route('/updateuser',methods=["GET","POST"])
def updateUser():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get("userid")
    nickname = data.get("nickname")
    password = data.get("password")
    headImg = data.get("headImg")
    gender = data.get("gender")
    infor = data.get("infor")

    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    # TODO 为什么这里要加引号
    c.execute("UPDATE usertable SET nickname = '{}',password = '{}',headImg = '{}',gender = '{}',infor = '{}' WHERE userid = {}".format(nickname,password,headImg,gender,infor,userid))

    conn.commit()
    conn.close()

    res = {}
    res["status"] = 1

    return res

@app.route('/showcarlist',methods=["GET","POST"])
def showCarList():
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM cartable WHERE ifcomplete = 0")
    res = {}
    restmp  = {}
    for row in cursor:
        restmp["carid"] = row[0]
        restmp["startpoint"] = row[1]
        restmp["endpoint"] = row[2]
        restmp["startdate"] = row[3]
        restmp["starttime"] = row[4]
        restmp["maxnum"] = row[5]
        restmp["price"] = row[6]
        restmp["userid_1"] = row[7]
        restmp["userid_2"] = row[8]
        restmp["userid_3"] = row[9]
        restmp["userid_4"] = row[10]
        restmp["remark"] = row[11]
        restmp["ifcomplete"] = row[12]

        res[str(row[0])] = restmp

    return res

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
