from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import dotenv
import logging
import os
from datetime import timedelta
from flask_socketio import SocketIO, emit, join_room

# from socket_server import app
from utils import image, text, audio, subtitles
from config import store
from config.db import db
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

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return 'Flask SocketIO server is Running'

@app.route("/api/python")
def hello_world():
  return "<p>Hello, World!</p>"

@app.route("/test/db")
async def func():
  random = db['random']
  random.drop()
  random.insert_one({'name': 'Jake', 'group': 'Enhypen'})
  obs = []
  for ob in random.find({}):
    obs.append(f"{ob['group']}: {ob['name']}")
  return jsonify({'data': obs})

# translation endpoints



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

# socket endpoints
onlineUsers = set()

@socketio.on('connect')
@jwt_required()
def handle_connect():
    print(f"Connected: {request.sid}")
    try:
      # token = request.args.get('auth', None)
      # if not token:
      #    print(f'Error: No authorisation token')
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
    onlineUsers.remove(user._id)


@socketio.on('custom_event')
def handle_custom_event(data):
    print(f"Received event: {data}")
    emit('response', {'message': 'Event received'})


if __name__ == "__main__":
  socketio.run(app, port=5328, debug=True)