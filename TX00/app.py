from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
app = Flask(__name__)
import time

# Channel Access Token
line_bot_api = LineBotApi("oa0d5+FU48SBc+ESyMJVzktZp6dXWVjhersqA5wEh4/QUp6imQHLJt8nGjYykJTpvJiYrIaUmAotsHeGfFDFR2aMrt9SYmc+5+aGuHSJ39Ehy4YX/i+k0RHGdsjW+zZCO5Qz07LburAhigapQOw3UQdB04t89/1O/w1cDnyilFU=")
# Channel Secret
channel_secret = "a12f70d38786bba699e3c864d679892e"
handler = WebhookHandler(channel_secret)
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    # handle webhook body   
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

uids = []
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    uid = event.source.user_id
    if os.path.isfile('uid.txt') is False:
        ff = open('uid.txt','a')
        ff.write(uid+'\n')
        ff.close()
        message = TextSendMessage(text="System add your ID")
        line_bot_api.reply_message(event.reply_token, message)
    else:
        f = [f.rstrip('\n') for f in open('uid.txt','r').readlines()]
        if uid not in f:
            ff = open('uid.txt','a')
            ff.write(uid+'\n')
            ff.close()
    # f = [f.rstrip('\n') for f in open('uid.txt','r').readlines()]
        message = TextSendMessage(text="System add your ID")
        line_bot_api.reply_message(event.reply_token, message)


pre_info = ""
pre_stat = []
while 1:
    fg = False
      
    if os.path.isfile('TX00-report.txt') is True:
        f = open('TX00-report.txt', 'r').readlines()
        print(len(f))
        if len(f) != 0:  
            new_list = []
            for ff in f:
                if ff.rstrip('\n') not in pre_stat:
                    new_list += [ff.rstrip('\n')]
            
            if new_list != []:
                message = TextSendMessage(text='\n'.join(new_list))
                ff = [f.rstrip('\n') for f in open('uid.txt','r').readlines()]
                line_bot_api.multicast(ff, message)
                pre_stat += new_list
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
