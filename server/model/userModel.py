import sqlite3

class userModel:

    #用户注册
    def signup_model(self,phone,password):
        #连接数据库
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()

        #执行SQL语句
        SQL = "SELECT userid from usertable where phone = '%s' " % phone
        user = c.execute(SQL)

        #判断phone是否存在
        user = list(user)
        phone_exist = True if len(user) else False

        res = {}
        #phone存在无法注册，返回0
        #phone不存在可注册，注册完毕返回1
        if phone_exist:
            res["status"] = '0'
        else:
            #执行插入语句，记得commit
            c.execute("INSERT INTO usertable(phone,password) VALUES (?,?)", (phone, password))
            conn.commit()
            res["status"] = '1'
        conn.close()

        return res

    #用户登录
    def login_model(self,phone,password):
        #连接数据库
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = c.execute("SELECT userid,phone,password from usertable where phone = '{}'".format(phone))

        cursor = list(cursor)

        res = {}
        #TODO 在view层判断数据格式
        if len(cursor):
            #手机号密码匹配成功，登录返回uid和状态
            if str(cursor[0][1]) == phone and str(cursor[0][2]) == password:
                res['status'] = '1'
                res['msg'] = '登录成功！'
                res['uid'] = cursor[0][0]
            else:
                res['status'] = '0'
                res['msg'] = '账号或密码错误，请重新登录！'
        else:
            res['status'] = '0'

        conn.close()

        return res

    #显示用户信息
    def showUserMes_model(self,userid):

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

    #修改用户信息
    #todo 没有东西修改的话保持原值（前端还是后端实现？？）
    def updateUser_model(self,nickname, password, headImg, gender, infor, userid):

        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        # TODO 为什么这里要加引号
        c.execute(
            "UPDATE usertable SET nickname = '{}',password = '{}',headImg = '{}',gender = '{}',infor = '{}' WHERE userid = {}".format(
                nickname, password, headImg, gender, infor, userid))

        conn.commit()
        conn.close()

        res = {}
        res["status"] = 1

        return res