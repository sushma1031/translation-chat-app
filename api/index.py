from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import dotenv
import logging
import os
from datetime import timedelta

from utils import image, text, audio, subtitles
from config import store
from config.db import db
from controllers import register_user, login_user, fetch_user, logout_user

dotenv.load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
jwt = JWTManager(app)

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

# user endpoints
@app.route("/api/register", methods=['POST'])
async def register():
  response = await register_user.register_user(request.json)
  # TODO: login user
  return response

@app.route("/api/login", methods=['POST'])
async def login():
  return login_user.validate(request.json.get('email'), request.json.get('password'))
  
@app.route("/api/users/<name>/details")
@jwt_required()
async def user_details(name):
  current_user = get_jwt_identity()
  response = fetch_user.fetch_user_details(current_user)
  return response

@app.route("/api/logout")
def logout():
  return logout_user.logout()


if __name__ == "__main__":
  app.run(debug=True, port=5328)