import os

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
app = Flask(__name__)

line_bot_api = LineBotApi("oa0d5+FU48SBc+ESyMJVzktZp6dXWVjhersqA5wEh4/QUp6imQHLJt8nGjYykJTpvJiYrIaUmAotsHeGfFDFR2aMrt9SYmc+5+aGuHSJ39Ehy4YX/i+k0RHGdsjW+zZCO5Qz07LburAhigapQOw3UQdB04t89/1O/w1cDnyilFU=")
channel_secret = "a12f70d38786bba699e3c864d679892e"
handler = WebhookHandler(channel_secret)
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    uid = event.source.user_id
    if os.path.isfile('uid.txt') is False:
        open('uid.txt', 'r').close()

    existedUID = open('uid.txt','r').read().splitlines()
    if uid not in existedUID:
        with open('uid.txt', 'a') as f:
            f.write(uid+'\n')

    message = TextSendMessage(text="System add your ID")
    line_bot_api.reply_message(event.reply_token, message)

prevSignal = []
while True:
    if os.path.isfile('TX00-report.txt') is True:
        signals = open('TX00-report.txt', 'r').read().splitlines()
        if len(signals) != 0 and len(prevSignal) != len(signals):
            newSiganl = [s for s in signals if s not in prevSignal]
            message = TextSendMessage(text='\n'.join(newSiganl))
            uids = open('uid.txt','r').read().splitlines()
            line_bot_api.multicast(uids, message)
            prevSignal = signals

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
