# app.py
from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS
from generateMap import generateMap
import db

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
   #db.createTables(r"./db/sqlite.db")
    return db.getClassements(r"./db/sqlite.db")


@app.route("/generate")
def generate():
    map = generateMap()
    return map


@app.route("/insertClassement", methods=["POST"])
def insertClassement():
    request_data = request.get_json()

    username = request_data['username']
    score = request_data['score']
    print(username)
    print(score)
    db.insertClassement(r"./db/sqlite.db", username, score)
    print(db.getClassements(r"./db/sqlite.db"))
    return Response("", status=201, mimetype='application/json')

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()
