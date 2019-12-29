from flask import Flask
from view.userView import user_view
from view.carView import car_view

class Config(object):
    DEBUG=True
    JSON_AS_ASCII=False

app = Flask(__name__)
#解决中文乱码的问题，将json数据内的中文正常显示
app.config['JSON_AS_ASCII'] = False
#开启debug模式
app.config['DEBUG'] = True
#从配置对象来加载配置
# app.config['JSON_AS_ASCII'] = False
# app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


app.register_blueprint(user_view)
app.register_blueprint(car_view)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    # app.config.from_object(Config)
    app.config['DEBUG'] = True

    app.config['JSON_AS_ASCII'] = False

    app.run(host="127.0.0.1", port=5050, debug=True)


