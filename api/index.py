from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os

from utils import image, text, audio, subtitles
from config import store
from config.db import db


app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/translate/text', methods=['POST'])
async def translate_text():
    

    # Return the translated text as a JSON response
    # trans = text.translate_text(t, 'korean', 'english')
    trans = 'dummy'
    return jsonify({'translated': trans})

@app.route("/api/translate/image", methods=['POST'])
async def translate_image():
  if 'file' not in request.files:
    return "No file part"
  file = request.files['file']
  
  src = request.form.get('src')
  dest = request.form.get('dest')
  save_path = os.path.join("uploads", file.filename)
  file.save(save_path)
  
  # translations = image.translate_img_text(save_path, src, dest)
  translations = ["Foo bar", "rab ooF"]
  # TODO upload image to cloudinary (or handle in FE?)
  os.remove(save_path)
  
  return jsonify({'translated': translations})

@app.route("/api/translate/audio", methods=['POST'])
async def translate_audio():
  file = request.files['file']
  src = request.form['src']   
  dest = request.form['dest']
  sp_text = ''
  # raise an error if no file
  save_path = os.path.join("uploads", file.filename)
  file.save(save_path)
  sp_text = audio.transcribe_audio(save_path, src)
    
  try:
    res = text.translate_text(sp_text, src, dest)
    # res = 'transcribed & translated text'
    voice = await audio.text_to_voice(res.text, dest, file.filename[:-4])
    url = store.upload_to_cld(voice, "audio")
    logging.debug('Successful.')
    os.remove(voice)
    return jsonify({'translated': url})
  except Exception as e:
    print(e)
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