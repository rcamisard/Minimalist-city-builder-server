# app.py
from flask import Flask
from generateMap import generateMap
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Coucou les zouz</p>"

@app.route("/generate")
def generate():
    map = generateMap()
    return map


if __name__ == '__main__':
    app.run()
