from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import image

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"