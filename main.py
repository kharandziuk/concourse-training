import os

from flask import Flask

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

APP_PORT = os.environ.get("APP_PORT", 80)


@app.route("/", methods=["GET"])
def index():
    return "Hello!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
