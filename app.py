from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)


line_bot_api = LineBotApi('wPa4+Ugu3xA08HNggnazzFkVI4y0U9OrdNyTIpC/5sGzFdi1MaTughkBirlLB/YE4OfMsyZrT5iB5QULE+r0jAQFDkI86OUhhCl3Ql2vFm+WUCrMXv9+pn00oNHRFERhsg5kRZ/joTQgd/d9JsqIhQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a11e8d23118f4adf0a09709163447b46')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()