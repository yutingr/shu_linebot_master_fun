from flask import Flask, request, abort

from linebot import (
        LineBotApi, WebhookHandler
)
from linebot.exceptions import (
        InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('8gJCs4UU2pCyEeWKiGM5H1goheoUCKIz362oIhO3Jr1jZFq4lG/OsRMEKCevFHa32E5FwXWmrNvVf2GowlG5xnCpHK9CzNa+7/d1U1isJkJOsVFCtR1egXyg9dHJOF4teGvK3UfA12VZg/Sokgqx6QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('db4369800ec743d6d3220de2f0b81868')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Button(event)
        Reply(event)
        line_bot_api.push_message("U2312c676dff3cdd882d4ebc0ff5d0450", TextSendMessage(text=event.source.user_id))
        line_bot_api.push_message("U2312c676dff3cdd882d4ebc0ff5d0450", TextSendMessage(text=event.message.text))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=str(e)))

# 回覆函式
def Reply(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U2312c676dff3cdd882d4ebc0ff5d0450":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
    else:
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text = Ktemp[1]))
        else:
            line_bot_api.reply_message(event.reply_token,
                                       Button(event))

# 處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "ID":
#        line_bot_api.reply_message(event.reply_token, 
#                                   TextSendMessage(text="外面下大雨!"))
        line_bot_api.push_message(event.source.user_id, TextSendMessage(text=event.source.user_id))

# 關鍵字系統
def KeyWord(text):
    KeyWordDict = {"你好":"今天天氣如何?",
                   "掰掰":"Bye Bye",
                   "我就點你!":"點屁啊!"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

# 按鈕版面系統
def Button(event):
    message = TemplateSendMessage(
            alt_text='請至智慧手機上確認訊息',  # 替代文字
            template=ButtonsTemplate(
                    # 開頭大圖
                    thumbnail_image_url='https://github.com/yutingr/linebot/blob/master/stitch1.jpg?raw=true',
                    title='Menu', 
                    text='Please select', 
                    actions=[
                            PostbackTemplateAction(
                                    label='找你的ID',
                                    data='ID'
                                    ),
                            MessageTemplateAction(
                                    label='點我啊~',
                                    text='我就點你!'
                                    ),
                            URITemplateAction(
                                    label='A.L.T_Life',
                                    uri='https://www.youtube.com/channel/UCcXyPDRksLQ7nBr_J2zEz-Q'
                                    )
                            ]
                    )
                )
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
