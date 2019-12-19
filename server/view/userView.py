import json
from flask import request,Blueprint
from model import userModel

user_view = Blueprint('user_view',__name__)
user_model = userModel.userModel

# phone:用户手机注册
# passwoerd：密码
#TODO:密码hash存储，手机号格式验证
@user_view.route('/signup', methods=["GET", "POST"])
def signup():
    #获取客户端json
    data = json.loads(request.get_data(as_text=True))
    phone = data.get('phone')
    password = data.get('password')

    #model层进行数据处理
    res = json.dumps(user_model.signup_model(user_model,phone,password))

    return res

# phone:用户手机注册
# passwoerd：密码
#TODO:手机号格式验证，多次登录验证，简单的安全登录
@user_view.route('/login', methods=["GET", "POST"])
def login():
    # 获取客户端json
    data = json.loads(request.get_data(as_text=True))
    phone = data.get('phone')
    password = data.get('password')

    res = json.dumps(user_model.login_model(user_model,phone,password))
    return res

#显示用户信息
#userid:用户id
@user_view.route('/showusermessage', methods=["GET", "POST"])
def showUserMes():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get("userid")

    res = json.dumps(user_model.showUserMes_model(userid))
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

