from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
import time
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    return resp

@socketio.on('message')
def handle_message(message):

    #画像送信
    with open("image.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    emit('message', {'type': 'image', 'data': encoded_image}, json=True)

    #文字列送信
    for character in message:
        emit('message', {'type': 'text', 'data': character}, json=True)
        time.sleep(1)

    #文字列送信終了
    emit('message', {'type': 'text', 'data': '<END_OF_MESSAGE>'}, json=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
