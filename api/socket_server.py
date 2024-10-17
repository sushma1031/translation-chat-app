from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

# Set up Socket.IO
# app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", async_mode='eventlet')

@app.route('/')
def index():
    return 'Flask SocketIO server is Running'

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('custom_event')
def handle_custom_event(data):
    print(f"Received event: {data}")
    socketio.emit('response', {'message': 'Event received'})