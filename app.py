from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from vendor import openWeatherApi

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('/aDdPdXosvKKMcWJ0vXbd0ZOvEyUEn7hzImpBqoxL5aC1VPY3YK3BULH/+fe3nBqttPStGy2vgdXf0J02ja5jRRuZSCdnaU5hc1MFGlH4MDmrSHENYtfa9oFpfdivffCA2TC9IZ6QAse/yxrj0J2CwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('074a0a8eaefb181417504c6d0e453178')

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

@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(event.postback.data)


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)

    print(event)
    print('-----------------------------')
    print(MessageEvent)

    if 'image' in event.message.text:
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/XftEQMC.jpg',
            preview_image_url='https://friendoprod.blob.core.windows.net/missionpics/images/4237/member/1bf3b1c2-413c-4454-8f23-965b96f1cc04.jpg'
        )
    elif '天氣' in event.message.text:
        message = TextSendMessage(text=openWeatherApi.get_weather())
    
    elif 'postback' in event.message.text:
        actions1 = []
        actions2 = []
        cols = []

        actions1.append(PostbackAction(label='Buy', data='action=buy&itemid=111', display_text=None, text=None))
        actions1.append(PostbackAction(label='Add to cart', data='action=add&itemid=111', display_text=None, text=None))
        actions1.append(URIAction(label='View detail', uri='http://example.com/page/111', alt_uri=None))

        actions2.append(PostbackAction(label='Buy', data='action=buy&itemid=222', display_text=None, text=None))
        actions2.append(PostbackAction(label='Add to cart', data='action=add&itemid=222', display_text=None, text=None))
        actions2.append(URIAction(label='View detail', uri='http://example.com/page/222', alt_uri=None))

        default_action = URIAction(label='View detail', uri='http://example.com/page/123', alt_uri=None)

        cols.append(CarouselColumn(text='Description 1', title='This is menu',
            thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wyzowl.com%2Fyoutube-thumbnail-size%2F&psig=AOvVaw0yepNJjwuioY2kEWmgntT8&ust=1582191783109000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLiZhe2p3ecCFQAAAAAdAAAAABAD', 
            image_background_color='#FFFFFF', actions=actions1, default_action=default_action))
        cols.append(CarouselColumn(text='Description 2', title='This is menu',
            thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wyzowl.com%2Fyoutube-thumbnail-size%2F&psig=AOvVaw0yepNJjwuioY2kEWmgntT8&ust=1582191783109000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLiZhe2p3ecCFQAAAAAdAAAAABAD', 
            image_background_color='#000', actions=actions2, default_action=default_action))

        message = CarouselTemplate(columns=cols, image_aspect_ratio='rectangle',
            image_size='cover')

    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
