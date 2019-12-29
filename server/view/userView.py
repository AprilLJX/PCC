import json
from flask import request,Blueprint
from model import userModel
import hashlib
import re
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from random import choice

client = AcsClient('LTAI4FoqkVAaNdyWkFNQv1Kk', 'DTfwoggcKGA3E3xQVwxP6pnkq34k7s', 'cn-hangzhou')

# 定义一个种子，从这里面随机拿出一个值，可以是字母
seeds = "1234567890"

user_view = Blueprint('user_view',__name__)
user_model = userModel.userModel

#验证码的全局变量
verifycodeDic = {}

def getSms():
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

    request.add_query_param('PhoneNumbers', "15387594636")

    response = client.do_action(request)
    # python2:  print(response)
    return random_str
    #print(str(response, encoding='utf-8'))

#@param：
#phone:用户手机注册
#passwoerd：密码
#function:为0表示获取验证码，为1表示注册,为2表示修改密码
#TODofinish:密码hash存储，手机号格式验证
#todo 手机号验证码
@user_view.route('/signup', methods=["GET", "POST"])
def signup():
    #获取客户端json
    data = json.loads(request.get_data(as_text=True))
    phone = str(data.get('phone'))
    password = str(data.get('password'))
    function = str(data.get('function'))
    verifycode = str(data.get("verifycode"))

    res = {}

    #判断数据是否为空
    if len(phone) == 0 or len(password) == 0:
        res['status'] = 0
        res['mag'] = "参数为空"
        return res

    #手机号格式验证
    pattern = re.compile('13[0,1,2,3,4,5,6,7,8,9]|15[0,1,2,7,8,9,5,6,3]|18[0,1,9,5,6,3,4,2,7,8]|17[6,7]|147\d{8}')
    pattern_true = pattern.match(str(phone))

    if not pattern_true:
        res["status"] = 0
        res["mag"] = "手机号格式错误"
        return res

    #function为0返回验证码
    if function == "0":
        verifycodeDic[phone] = getSms()
        res["verifycode"] = verifycodeDic[phone]
        return res

    #function为1代表注册，判断验证码是否一致
    if function == "1":
        if verifycode == verifycodeDic[phone]:
            # 密码加密
            depassword = hashlib.md5()
            depassword.update(password.encode('utf-8'))
            depassword = depassword.hexdigest()

            # model层进行数据处理
            res = json.dumps(user_model.signup_model(user_model, phone, depassword))

            return res
        else:
            res["status"] = 0
            res["msg"] = "验证码错误"
            return res


# phone:用户手机注册
# passwoerd：密码
#TODOfinish:手机号格式验证，多次登录验证，简单的安全登录
#todo 多次登录验证
@user_view.route('/login', methods=["GET", "POST"])
def login():
    # 获取客户端json
    data = json.loads(request.get_data(as_text=True))
    phone = str(data.get('phone'))
    password = str(data.get('password'))

    res = {}
    #todo 这里太冗余了，代码跟上面的一样
    #判断数据是否为空
    if len(phone) == 0 or len(password) == 0:
        res['status'] = 0
        res['mag'] = "参数为空"
        return res

    # 手机号格式验证
    pattern = re.compile('13[0,1,2,3,4,5,6,7,8,9]|15[0,1,2,7,8,9,5,6,3]|18[0,1,9,5,6,3,4,2,7,8]|17[6,7]|147\d{8}')
    pattern_true = pattern.match(str(phone))

    if not pattern_true:
        res["status"] = 0
        res["mag"] = "手机号格式错误"
        return res

    #密码加密后与数据库匹配
    depassword = hashlib.md5()
    depassword.update(password.encode('utf-8'))
    depassword = depassword.hexdigest()


    res = json.dumps(user_model.login_model(user_model,phone,depassword))
    return res

#显示用户信息
#userid:用户id
@user_view.route('/showusermessage', methods=["GET", "POST"])
def showUserMes():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get("userid")
    res = {}

    if type(userid) != int:
        res["status"] = 0
        res["msg"] = "格式错误"
        return res


    res = json.dumps(user_model.showUserMes_model(user_model,userid))
    return res

#修改用户信息
#userid: 用户id
#nickname: 用户昵称
#password: 用户密码
#headImg: 用户头像
#gender： 性别
#infor：个性签名
#todo 头像
#TODO 修改密码，输入原密码，修改密码之后重新输入确认
@user_view.route('/updateuser', methods=["GET", "POST"])
def updateUser():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get("userid")
    nickname = data.get("nickname")
    password = data.get("password")
    headImg = data.get("headImg")
    gender = data.get("gender")
    infor = data.get("infor")


    res = user_model.updateUser_model(user_model,nickname,password,headImg,gender,infor,userid)

    return res

