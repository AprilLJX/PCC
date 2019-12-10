import sqlite3
import json

from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route('/signup',methods=["GET","POST"])
def signup():
    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()

    data = json.loads(request.get_data(as_text=True))
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

@app.route('/start_carpool',methods=["GET","POST"])
def startCar():
    data = json.loads(request.get_data(as_text=True))
    startpoint = data.get('startpoint')
    endpoint = data.get('endpoint')
    startdate = data.get('startdate')
    starttime = data.get('starttime')
    maxnum = data.get('num')
    userid_1 = data.get('userid_1')

    remark = data.get('remark')

    conn = sqlite3.connect("data/pccDB.db")
    c = conn.cursor()
    c.execute("INSERT INTO cartable(startpoint,endpoint,startdate,starttime,maxnum,userid_1,remark) "
              "VALUES (?,?,?,?,?,?,?)", (startpoint,endpoint,startdate,starttime,maxnum,userid_1,remark))
    carid = c.lastrowid
    conn.commit()
    conn.close()

    res = {}
    res['carid'] = carid

    return res





if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
