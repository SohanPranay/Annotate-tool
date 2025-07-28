import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', data, broadcast=True)

@socketio.on('draw')
def handle_draw(data):
    emit('draw', data, broadcast=True)

@socketio.on('clear_canvas')
def handle_clear_canvas():
    emit('clear_canvas', broadcast=True)

# Only use this if running locally
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render will set $PORT
    print(f"Server is starting on http://0.0.0.0:{port}")
    socketio.run(app, host='0.0.0.0', port=port)
