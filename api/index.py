from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import dotenv
import os
import sys
from datetime import timedelta
from flask_socketio import SocketIO, emit, join_room

from utils import image, text, audio, subtitles
from controllers import register_user, login_user, fetch_user, logout_user

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}, 
                     r"/socket.io/*": {"origins": "http://localhost:3000"}}, 
                     supports_credentials=True)
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']

jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", async_mode='eventlet')

@app.route('/')
def index():
    return 'Flask SocketIO server is Running'

# translation endpoints
@app.route('/api/translate/text', methods=['POST'])
async def translate_text():
  """
  src: source language code
  dest: destination language code
  text: text to be translated
  """
  data = request.get_json()
  src = data['src']   
  dest = data['dest']
  url = data['text']
  result = text.translate_text(url, src, dest)
  if result.get('success', False):
     return jsonify(result), 200
  return jsonify(result), 500

@app.route("/api/translate/image", methods=['POST'])
async def translate_image():
  """
  src: source language code
  dest: destination language code
  url: url of media
  """
  data = request.get_json()
  src = data['src']   
  dest = data['dest']
  url = data['url']
  
  result = image.download_and_translate_img(url, src, dest)
  if result.get('success', False):
     return jsonify(result), 200
  return jsonify(result), 500

@app.route("/api/translate/audio", methods=['POST'])
async def translate_audio():
  """
  src: source language code
  dest: destination language code
  url: url of media
  """
  data = request.get_json()
  src = data['src']   
  dest = data['dest']
  url = data['url']
  result = audio.translate_and_upload_audio(url, src, dest)
  if result.get('success', False):
     return jsonify(result), 200
  return jsonify(result), 500
    

@app.route("/api/translate/subtitles", methods=['POST'])
async def generate_subtitles():
  data = request.get_json()
  src = data['src']   
  # dest = data['dest']
  url = data['url']
  result = subtitles.generate_st_and_upload(url, src)
  if result.get('success', False):
     return jsonify(result), 200
  return jsonify(result), 500

# user endpoints
@app.route("/api/register", methods=['POST'])
async def register():
  response = await register_user.register_user(request.json)
  # TODO: login user
  return response

@app.route("/api/login", methods=['POST'])
async def login():
  return login_user.validate(request.json.get('email'), request.json.get('password'))
  
@app.route("/api/user-details")
@jwt_required()
async def user_details():
  current_user = get_jwt_identity()
  response = fetch_user.fetch_user_details(current_user)
  return response

@app.route("/api/logout")
def logout():
  return logout_user.logout()

# socket endpoints
onlineUsers = set()

@socketio.on('connect')
@jwt_required()
def handle_connect():
    print(f"Connected: {request.sid}")
    try:
      identity = get_jwt_identity()
      user = fetch_user.fetch_user_by_email(identity["email"])
      if user:
        join_room(user["_id"])
        onlineUsers.add(user["_id"])
        emit('user_online', list(onlineUsers))
    except Exception as e:
       print(f'Error connecting user: {e}')


@socketio.on('disconnect')
@jwt_required()
def handle_disconnect():
    print(f'Disconnected: {request.sid}')
    token = get_jwt_identity()
    user = fetch_user.fetch_user_by_email(token["email"])
    onlineUsers.discard(user["_id"])


@socketio.on('chat')
def handle_chat(userId):
    from models.User import users
    from bson.objectid import ObjectId
    # print(f"Received data: {userId}", file=sys.stdout)
    user = users.find_one({"_id": ObjectId(userId)}, {"password": 0})
    payload = {
       "_id": str(user["_id"]),
       "name": user["name"],
       "email": user["email"],
       "language": user["language"],
       "profile_pic": user["profile_pic"],
       "online": (userId in onlineUsers)
    }
    emit("user_status", payload)

@socketio.on('new_message')
def handle_new_message(data):
  print(f"data: {data}", file=sys.stdout)
  from models.Chat import chats, messages, Chat, Message
  from bson.objectid import ObjectId

  #  check if there exists a Chat b/w sender & receiver in the db
  sender_id = ObjectId(data['sender'])
  receiver_id = ObjectId(data['receiver'])
  # print(f"{sender_id}, {receiver_id}", file=sys.stdout)
  
  chat = chats.find_one({
    "$or": [
        { "sender": sender_id, "receiver": receiver_id },
        { "sender": receiver_id, "receiver": sender_id }
    ]
  })
  
  if not chat:
    new_chat = Chat(sender=ObjectId(data["sender"]), receiver=ObjectId(data["receiver"]))
    result = chats.insert_one(new_chat.model_dump())
    chat = chats.find_one({'_id': result.inserted_id})
  
  new_message = Message(original_lang=data["src_lang"], 
                        text=data["text"], 
                        translated_text="", trans_audio_url="", trans_video_url="", 
                        image_url=data["imageUrl"], audio_url=data["audioUrl"], video_url=data["videoUrl"], 
                        user_id=sender_id)
  
  # message = messages.find_one({'_id': mresult.inserted_id})
  
  # TODO translate message and update that
  src_code = data["src_lang"]
  dest_code = data["dest_lang"]
  if not (src_code == dest_code):
    if data["text"]:
      result = text.translate_text(data["text"], src_code, dest_code)
      if result.get('success', False):
          new_message["trans_text"] = result.get('result')
    elif data["audioUrl"]:
      result = audio.translate_and_upload_audio(data["audioUrl"], src_code, dest_code)
      if result.get('success', False):
          new_message["trans_audio_url"] = result.get('result')
    elif data["imageUrl"]:
      result =  image.download_and_translate_img(data["imageUrl"], src_code, dest_code)
      if result.get('success', False):
          new_message["trans_text"] = "; ".join(result.get('result'))
    elif data["videoUrl"]:
      result = subtitles.generate_st_and_upload(data["videoUrl"], src_code)
      if result.get('success', False):
          new_message["trans_video_url"] = result.get('result')

  mresult = messages.insert_one(new_message.model_dump())
  message = messages.find_one({'_id': mresult.inserted_id})
  # TODO update conversation
  # TODO translate message and update that
  # TODO fetch messages (not ids!) from the conversation
  # TODO emit to both sender and receiver
  emit('message', ["a whole bunch of messages"], to=data["sender"])
  emit('message', ["a whole bunch of messages"], to=data["receiver"])

if __name__ == "__main__":
  socketio.run(app, port=5328, debug=True)