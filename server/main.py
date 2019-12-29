from flask import Flask
from view.userView import user_view
from view.carView import car_view


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(user_view)
app.register_blueprint(car_view)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)


