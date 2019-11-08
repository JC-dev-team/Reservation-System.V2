from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def linebot_send_msg(line_id):
    try:
        text="<h1>Hello World</h1>"

        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # push message to one user
        line_bot_api.push_message(line_id, TextSendMessage(text=text))
        return 'success'
    except Exception as e:
        print(e)
        return 'failure'
    
