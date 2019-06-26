# Line Bot + Python 教學 #

## 1-1 事前準備
請先註冊以下兩個網站的帳號  
Github:https://github.com  
Heroku:https://heroku.com

## 1-2 上架範例程式

## 2-1 流程解說
我們可以將Line想像成一個傳遞對話的傳聲筒，  
當使用者傳送文字給我們的Line帳號時，  
程式會收到一個包含使用者ID、他傳送的文字等等的資料包，  
然後再根據我們寫的程式去處理這些資料，  
最後回覆給Line一個我們製作的資料包，  
然後Line根據我們的資料包來回覆使用者。  
而我們回復使用者的程式則要寫在範例程式第35行的handle_message(event)函式中。  
現在我們來看看這段程式：

    def handle_message(event):
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
第一行括號內的引數event是前文所述程式收到的資料，  
而第二行宣告一個變數message，並在裡面放入一個「訊息物件」  
訊息物件是什麼呢？  
就像Line傳給我們的資料Event裡包含很多資料一樣，  
我們要回傳給Line的資料包裡也要包含很多資料，  
而製作這些資料包的方法就是第二行的TextSendMessage()函式。  

    TextSendMessage(text=event.message.text)
在這裡我們設定訊息物件裡的text項目為event.message.text，  
這個event.message.text就是Line傳給我們的資料包event中使用者輸入的話，  
這次我們直接將使用者傳來的話打包成訊息物件，  
沒有經過任何處理，  
因此使用者輸入什麼文字，我們都會原封不動的傳回去。  
接著解釋第三行程式：

    line_bot_api.reply_message(event.reply_token, message)
這一行呼叫了Line提供的「回覆 reply」方法，  
第一個引數event.reply_token一樣來自Line傳給我們的資料包，  
它就像是一種密鑰，告訴Line我們是對的人，  
每觸發一次使用者輸入文字的事件，都會產生一個新的密鑰。  
第二個引數message是我們要傳送的訊息物件。  
一個基本的文字處理就這樣結束了，  
我們接到event資料包後把使用者輸入的話用TextSendMessage()重新打包，  
然後用line_bot_api.reply_message()傳回去，  
因此現在我們的機器人只是一個人云亦云的學舌鳥而已。

## 2-2 小試身手
現在我們試著修改範例程式，  
讓我們的程式可以對某些關鍵字有所反應。  
