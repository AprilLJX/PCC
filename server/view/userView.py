import json
from flask import request,Blueprint
from model import userModel
import re


user_view = Blueprint('user_view',__name__)
user_model = userModel.userModel

#@param：
#phone:用户手机注册
#passwoerd：密码
#function:为0表示获取验证码，为1表示注册,为2表示修改密码
#TODofinish:密码hash存储，手机号格式验证
#todofinish 手机号验证码
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

    res = json.dumps(user_model.signup_model(user_model, phone, password,function,verifycode))

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

    res = json.dumps(user_model.login_model(user_model,phone,password))
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
    headImg = data.get("headImg")
    gender = data.get("gender")
    infor = data.get("infor")

    res = user_model.updateUser_model(user_model,nickname,headImg,gender,infor,userid)

    return res
#修改密码
#@param：
# phone：电话
# password：密码
# function: 0为发送验证码，1为修改密码
# verifycode：验证码
@user_view.route('/updatePassword',methods=["GET", "POST"])
def updatePwd():
    data = json.loads(request.get_data(as_text=True))
    phone = str(data.get("phone"))
    password = str(data.get("password"))
    function = str(data.get("function"))
    verifycode = str(data.get("verifycode"))

    res = {}

    #判断用户是否存在
    if not user_model.updatePwd_model(user_model,phone):
        res["status"] = 0
        res["msg"] = "账号不存在"
        return res






