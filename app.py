import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
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
line_bot_api = LineBotApi('N9Mkh2LWR7Yk62DKXf83OLW8Kubyv4gWjYNhJsP15pIyqcsxgr/uTTFOsFiq7SDdQksZjfyBbGRXUhpywRzIMDRxDlfS2Q4E1EEYWHZX1iZ4xXi2LTGYRKDE7QV7AtOAZ+TcI/LjUdgu5IC7bHEIQQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7db431691746e4fecfb09baca6d5dc74')

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
        # message = TextSendMessage(text=event.message.text)
        # line_bot_api.reply_message(event.reply_token, message)

        if event.message.text != "":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
            pass
            #GDriveJSON就輸入下載下來Json檔名稱
            #GSpreadSheet是google試算表名稱
            GDriveJSON = 'MasterFun-9e0316c16434.json'
            GSpreadSheet = '流行語資料庫'
            while True:
                try:

                    # scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
                    # creds = ServiceAccountCredentials.from_json_keyfile_name("./GoogleSheetTeach-WP-2c572cd3d8d0.json", scope)
                    # client = gspread.authorize(creds)

                    # spreadSheet = client.open("流行語資料庫")#或是可以用 add_worksheet("11月", 100, 100) 來新增

                    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
                    key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                    gc = gspread.authorize(key)
                    worksheet = gc.open(GSpreadSheet).sheet1
                except Exception as ex:
                    print('無法連線Google試算表', ex)
                    sys.exit(1)
                textt=""
                textt+=event.message.text
                if textt!="":
                    worksheet.append_row((datetime.datetime.now(), textt))
                    print('新增一列資料到試算表' ,GSpreadSheet)
                    return textt          
        # Button(event)
        # Reply(event)
        # line_bot_api.push_message("U64ed76c0eed306e3050055c90acca990", TextSendMessage(text=event.source.user_id))
        # line_bot_api.push_message("U64ed76c0eed306e3050055c90acca990", TextSendMessage(text=event.message.text))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=str(e)))

# 回覆函式
def Reply(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U64ed76c0eed306e3050055c90acca990":
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
