from flask import Flask,Blueprint,request
from model import carModel
import json

car_view = Blueprint('car_view',__name__)
car_model = carModel.carModel

#发起拼车
#startpoint：起点
#endpoint：终点
#startdate：日期
#starttime：时间
#num：需要拼车人数
#price：预计价格
#userid_1：发起人userid
#remark：备注信息
#todo 数据提前处理
@car_view.route('/startcarpool', methods=["GET", "POST"])
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

    res = json.dumps(car_model.startCar_model(carModel))
    return res

#加入拼车
#carid：所加入的拼车单的id
#userid：申请加入该拼车的用户
#todo 怎么保证是该用户申请的（当前用户可以直接通过该url实现功能）
@car_view.route('/joincarpool', methods=["GET", "POST"])
def joinCar():
    data = json.loads(request.get_data(as_text=True))
    carid = data.get('carid')
    userid = data.get('userid')

    res = json.dumps(car_model.joinCar_model(car_model,carid,userid))
    return res


#退出拼车
#userid：申请退出拼车的用户
#carid：拼车单的单号
@car_view.route('/exitcarpool', methods=["GET", "POST"])
def exitCar():
    data = json.loads(request.get_data(as_text=True))
    userid = data.get('userid')
    carid = data.get('carid')

    res = json.dumps(car_model.exitCar_model(car_model,userid,carid))

    return res


#显示所有的拼车信息
@car_view.route('/showcarlist', methods=["GET", "POST"])
def showCarList():

    res = json.dumps(car_model.showCarList_model)
    return res
