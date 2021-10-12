# app.py
from flask import Flask
from generateMap import generateMap
import db
app = Flask(__name__)

@app.route("/")
def hello_world():
    db.createTables(r"./db/sqlite.db")
    return db.getClassements(r"./db/sqlite.db")


@app.route("/generate")
def generate():
    map = generateMap()
    return map


@app.route("/insertClassement", methods=['POST'])
def insertClassement():
    username = request.args.get("username")
    points = request.args.get("points")
    db.insertClassement(r"./db/sqlite.db", username, points)
    return 200


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()
