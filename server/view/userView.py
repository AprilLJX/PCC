import json
from flask import request,Blueprint
from model import userModel

user_view = Blueprint('user_view',__name__)



@user_view.route('/signup', methods=["GET", "POST"])
def signup():
    # data1 = request.get_json(force=True)
    # data = ()
    # print(type(data))

    data = json.loads(request.get_data(as_text=True))
    phone = data.get('phone')
    password = data.get('password')

    user_model = userModel.userModel
    res = json.dumps(user_model.signup_model(user_model,phone,password))

    return res
    # return "singup"
