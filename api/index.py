from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import image, text, audio, subtitles
import store
import logging


app = Flask(__name__)
app.config['DEBUG'] = True
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

@app.route("/api/translate/audio", methods=['POST'])
async def translate_audio():
  # file = request.files['file']
  src = request.form['src']   
  dest = request.form['dest']
  sp_text = ''
  # raise an error if no file
  file = f"api/assets/hindi-2.wav"
  # sp_text = audio.transcribe_audio(file, src)
    
  try:
    # res = text.translate_text(sp_text, src, dest)
    # res = 'transcribed & translated text'
    # voice = audio.text_to_voice(res, dest, 'x')
    voice = 'cloudinary link of translated audio msg'
    logging.debug('Successful.')
    return jsonify({'translated': voice})
  except Exception as e:
    logging.debug(e)
    return jsonify({'translated': f"error: {e}"})

@app.route("/api/translate/subtitles", methods=['POST'])
async def generate_subtitles():
  # src = request.form['src']   
  # dest = request.form['dest']
  logging.debug("here")
  path = "api/assets/hindi-2.wav"
  result = store.upload_to_cld(path, "audio")
  ...
  return jsonify({'data': result})