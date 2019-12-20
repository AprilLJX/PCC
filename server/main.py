from flask import Flask
from view.userView import user_view
from view.carView import car_view


app = Flask(__name__)
app.register_blueprint(user_view)
app.register_blueprint(car_view)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)


