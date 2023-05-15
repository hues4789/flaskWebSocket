from flask import Flask, Response, render_template, request, json, make_response
import time
import queue
import uuid

app = Flask(__name__)

messages = {}

#ユーザーが一定時間active出ない場合キュー削除
#user_last_activity = {}
#

@app.route('/')
def index():
    #ユーザーごとに処理を分けるため、固有のIDをcookieに持たせる
    user_id = str(uuid.uuid4())
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user_id', user_id)
    #固有のIDごとのキューを持たせる
    messages[user_id] = queue.Queue()

    #ユーザーが一定時間active出ない場合キュー削除
    #user_last_activity[user_id] = datetime.now()
    #

    return resp

@app.route('/send', methods=['POST'])
def send():
    #messageと固有のIDを取得
    data = json.loads(request.data)
    message = data.get('message')
    user_id = request.cookies.get('user_id')
    #ここを適切な処理に変更　（今回はmessageを一文字ずつ区切りキューに入れる（１秒待つ））
    for character in message:
        messages[user_id].put(character)
        time.sleep(1)
    #ユーザーが一定時間active出ない場合キュー削除
    #user_last_activity[user_id] = datetime.now() 
    #

    return '', 204

@app.route('/stream')
def stream():
    user_id = request.cookies.get('user_id')
    def event_stream():
        while True:
            #ユーザーが一定時間active出ない場合キュー削除
            # if datetime.now() - user_last_activity[user_id] > timedelta(hours=3):
            #     # Delete user's message queue
            #     del messages[user_id]
            #     del user_last_activity[user_id]
            #     break

            #キューに値がある場合は、front側へ送信
            message = messages[user_id].get()
            yield f"data: {message}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
