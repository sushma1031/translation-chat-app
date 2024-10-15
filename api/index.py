from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import image, text, audio

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/translate/text', methods=['POST'])
async def translate_text():
    data = request.get_json() # Get JSON data from the request
    t = data.get('text') # Extract the text sent from React

    # Return the translated text as a JSON response
    # trans = text.translate_text(t, 'korean', 'english')
    trans = 'dummy'
    return jsonify({'translated': trans})

@app.route("/api/translate/image", methods=['POST'])
async def translate_image(): 
  path = f"api/assets/kannada-1.jpg"
  
  # translations = image.translate_img_text(path, 'kannada', 'english')
  translations = ["Foo bar", "rab ooF"]
  
  return jsonify({'translated': translations})

@app.route('/api/translate/text', methods=['POST'])
def translate_text():
    data = request.get_json()  # Get JSON data from the request
    text = data.get('text')    # Extract the text sent from React

    # Return the translated text as a JSON response
    return jsonify({'translated': text})