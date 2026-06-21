from flask import Flask 

web_app = Flask(__name__)
@web_app.route("/hello", methods=["GET"])
def hello():
    return "Hello, World! from flaskapi"
if __name__ == "__main__":
    web_app.run(debug=True)

