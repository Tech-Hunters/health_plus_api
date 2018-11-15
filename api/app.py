import json
from flask import Flask, Response, abort

app = Flask(__name__)

@app.route('/')
def index():
    return "wow"

