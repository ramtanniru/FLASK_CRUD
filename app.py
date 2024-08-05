from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello world"

@app.route("/home")
def home():
    return "Hello Home"

@app.route("/user")
def user():
    return "Hello user"
from controller import *