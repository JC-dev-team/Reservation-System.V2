from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def linebot_send_msg(line_id):
    try:
        text="<h1>Hello World</h1>"

        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # push message to one user
        
        line_bot_api.push_message('U5ee811f1f2f899eb66844500ef14a371', TextSendMessage(text='1'))
        line_bot_api.push_message('Uf7e1093512c0dac60f60974ff53e4a2c', TextSendMessage(text='2'))
        
        
        
        return 'success'
    except Exception as e:
        return 'failure'
    
