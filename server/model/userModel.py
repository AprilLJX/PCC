import sqlite3
import hashlib
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from random import choice

client = AcsClient('', '', 'cn-hangzhou')

# 定义一个种子，从这里面随机拿出一个值，可以是字母
seeds = "1234567890"
#验证码的全局变量
verifycodeDic = {}

class userModel:

    def getSms(self,phone):
        # 定义一个空列表，每次循环，将拿到的值，加入列表
        random_num = []
        # choice函数：每次从seeds拿一个值，加入列表
        for i in range(4):
            random_num.append(choice(seeds))
        # 将列表里的值，变成四位字符串
        random_str = "".join(random_num)
        code = "{\"code\":\"" + random_str + "\"}"
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('SignName', "拼车车")
        request.add_query_param('TemplateCode', "SMS_181501054")
        request.add_query_param('TemplateParam', code)

        request.add_query_param('PhoneNumbers', phone)

        response = client.do_action(request)
        # python2:  print(response)
        return random_str
        # print(str(response, encoding='utf-8'))

    #用户注册
    def signup_model(self,phone,password,function,verifycode):

        res = {}
        # function为0返回验证码
        if function == "0":
            verifycodeDic[phone] = self.getSms(self,phone)
            res["verifycode"] = verifycodeDic[phone]
            return res

        # function为1代表注册，判断验证码是否一致
        if function == "1":
            if verifycode == verifycodeDic[phone]:
                # 密码加密
                depassword = hashlib.md5()
                depassword.update(password.encode('utf-8'))
                depassword = depassword.hexdigest()
                # 连接数据库
                conn = sqlite3.connect("data/pccDB.db")
                c = conn.cursor()

                # 执行SQL语句
                SQL = "SELECT userid from usertable where phone = '%s' " % phone
                user = c.execute(SQL)

                # 判断phone是否存在
                user = list(user)
                phone_exist = True if len(user) else False

                # phone存在无法注册，返回0
                # phone不存在可注册，注册完毕返回1
                if phone_exist:
                    res["status"] = '0'
                else:
                    # 执行插入语句，记得commit
                    c.execute("INSERT INTO usertable(phone,password) VALUES (?,?)", (phone, password))
                    conn.commit()
                    res["status"] = '1'
                conn.close()

                return res

            else:
                res["status"] = 0
                res["msg"] = "验证码错误"
                return res



    #用户登录
    def login_model(self,phone,password):

        # 密码加密后与数据库匹配
        depassword = hashlib.md5()
        depassword.update(password.encode('utf-8'))
        depassword = depassword.hexdigest()

        #连接数据库
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        cursor = c.execute("SELECT userid,phone,password from usertable where phone = '{}'".format(phone))

        cursor = list(cursor)

        res = {}

        if len(cursor):
            #手机号密码匹配成功，登录返回uid和状态
            if str(cursor[0][1]) == phone and str(cursor[0][2]) == depassword:
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
    def updateUser_model(self,nickname, headImg, gender, infor, userid):

        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        # TODO  为什么这里要加引号
        c.execute(
            "UPDATE usertable SET nickname = '{}',headImg = '{}',gender = '{}',infor = '{}' WHERE userid = {}".format(
                nickname, headImg, gender, infor, userid))

        conn.commit()
        conn.close()

        res = {}
        res["status"] = 1

        return res

    #修改密码
    def updatePwd_model(self,phone,password,function,verifycode):
        conn = sqlite3.connect("data/pccDB.db")
        c = conn.cursor()
        SQL = "SELECT userid from usertable where phone = '%s' " % phone

        res = {}

        user = c.execute(SQL)

        # 判断phone是否存在
        user = list(user)
        phone_exist = True if len(user) else False
        if not phone_exist:
            res["status"] = 0
            res["msg"] = "账号不存在"
            return res

        # function为0返回验证码
        if function == "0":
            verifycodeDic[phone] = self.getSms(self,phone)
            res["verifycode"] = verifycodeDic[phone]
            return res

        # function为1判断验证码是否一致
        if function == "1":
            if verifycode == verifycodeDic[phone]:
                # 密码加密
                depassword = hashlib.md5()
                depassword.update(password.encode('utf-8'))
                depassword = depassword.hexdigest()
                # 连接数据库
                conn = sqlite3.connect("data/pccDB.db")
                c = conn.cursor()

                # 执行SQL语句
                SQL = "UPDATE usertable SET password = '{}' WHERE phone = '{}'".format(depassword, phone)
                c.execute(SQL)
                conn.commit()
                conn.close()
                res["status"] = 1
                res["msg"] = "修改成功"
                return res

            else:
                res["status"] = 0
                res["msg"] = "验证码错误"
                return res







