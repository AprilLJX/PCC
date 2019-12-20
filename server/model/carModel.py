import sqlite3

class carModel:

    def startCar_model(self,startpoint,endpoint,startdate,starttime,maxnum,price,userid_1,remark):

        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        c.execute("INSERT INTO cartable(startpoint,endpoint,startdate,starttime,maxnum,price,userid_1,remark) "
                  "VALUES (?,?,?,?,?,?,?,?)",
                  (startpoint, endpoint, startdate, starttime, maxnum, price, userid_1, remark))
        carid = c.lastrowid
        conn.commit()
        conn.close()

        res = {}
        res['msg'] = '发起拼车成功'
        res['carid'] = carid

        return res

    def joinCar_model(self,carid,userid):
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
        c.execute(
            "UPDATE cartable SET currentnum = {},{}={} WHERE carid = '{}'".format(currentnum, useradd, userid, carid))
        conn.commit()
        conn.close()

        res["status"] = 1
        res['msg'] = "加入拼车成功"
        return res

    def exitCar_model(self,userid,carid):
        res = {}
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = list(
            c.execute(
                "SELECT userid_1,userid_2,userid_3,userid_4,currentnum FROM cartable WHERE carid = {}".format(carid)))
        #当前人数为1，表示当前拼车只有一个人，退出即表示删除该订单
        #todo 如何保证退出的拼车单中存在该用户
        if cursor[0][4] == 1:
            c.execute("UPDATE cartable SET currentnum = 0,ifdelete = 1  WHERE carid = {}".format(carid))
            res["status"] = "删除成功"

            conn.commit()
            conn.close()
            return res
        #若退出的为发起的人，则将所有用户前移
        if str(cursor[0][0]) == userid:
            c.execute("UPDATE cartable SET userid_1 = {},userid_2 = {},userid_3 = {}, userid_4 = NULL,currentnum = {}"
                      " WHERE carid = {}".format(cursor[0][1],cursor[0][2],cursor[0][3],cursor[0][4] - 1,carid))
            res["status"] = "删除成功"
        elif str(cursor[0][1]) == userid:


            c.execute("UPDATE cartable SET userid_2 = '{}',userid_3 = '{}',userid_4 = NULL,currentnum = '{}' WHERE carid = '{}'".format(cursor[0][2], cursor[0][3] ,cursor[0][4] - 1 , carid))
            res["msg"] = "退出拼车成功"
            res["stratus"] = 1
        elif str(cursor[0][2]) == userid:
            c.execute(
                "UPDATE cartable SET userid_3 = {}, userid_4 = NULL,currentnum = {}"
                      " WHERE carid = {}".format(cursor[0][3],cursor[0][4] - 1,carid))
            res["status"] = "退出拼车成功"
        elif str(cursor[0][3]) == userid:
            c.execute(
                "UPDATE cartable SET userid_4 = NULL,currentnum = {}"
                      " WHERE carid = {}".format(cursor[0][4] - 1,carid))
            res["status"] = "退出拼车成功"
        else:
            res["status"] = "失败，没有权限"

        conn.commit()
        conn.close()

        return res

    def showCarList_model(self):
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = c.execute("SELECT * FROM cartable WHERE ifcomplete = 0 and ifdelete = 0")
        res = {}
        restmp = {}
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