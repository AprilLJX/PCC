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

    def selectCar_model(self, carid):
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = c.execute("SELECT * FROM cartable WHERE carid = '{}'".format(carid))
        cursor = list(cursor)

        res = {}
        res["car"] = cursor

        userlist = []
        reslist = []
        userlist.append(cursor[0][8])
        userlist.append(cursor[0][9])
        userlist.append(cursor[0][10])
        userlist.append(cursor[0][11])

        for user in userlist:
            if user:
                reslist.append(list(c.execute("SELECT userid,nickname, phone,headImg, gender,infor FROM usertable WHERE userid = '{}'".format(user)))[0])

        res["user"] = reslist

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

    #边际距离算法
    def minDistance(self,word1, word2):
        n1 = len(word1)
        n2 = len(word2)
        dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
        # 第一行
        for j in range(1, n2 + 1):
            dp[0][j] = dp[0][j - 1] + 1
        # 第一列
        for i in range(1, n1 + 1):
            dp[i][0] = dp[i - 1][0] + 1
        for i in range(1, n1 + 1):
            for j in range(1, n2 + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1
        # print(dp)
        return dp[-1][-1]

    #搜索拼车信息
    def searchCar_model(self,date,startpoint,endpoint):
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = c.execute("SELECT * FROM cartable WHERE ifcomplete = 0 and ifdelete = 0")
        cursor = list(cursor)

        restmp = {}
        carList = []
        resList = {}
        for row in cursor:
            #第一轮查询当前日期的所有订单
            if row[3] == date:
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
                carList.append(restmp)

        #计算距离
        for car in carList:
            startDis = self.minDistance(self,startpoint,car["startpoint"])
            endDis = self.minDistance(self,endpoint,car["endpoint"])

            car["dis"] = startDis + endDis

        carList = sorted(carList, key=lambda x: x["dis"])
        return carList














