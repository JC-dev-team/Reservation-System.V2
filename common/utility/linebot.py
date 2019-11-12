from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage


def linebot_send_msg(line_id, user=None,info=None):
    try:
        if info.time_session == "Dinner":
            time_session = '晚餐'
        else:
            time_session = '午餐'
        if info.is_confirm :
            is_confirm ='已確認'
        else :
            is_confirm ='待確認'

        text = "<h1>Hello World</h1>"
        flex ={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "SoftWay 訂位處理中",
                            "size": "xl",
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "預約",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": user.username+' '+info.adult+'大'+info.children+'小',
                                            "flex": 5,
                                            "size": "sm",
                                            "color": "#666666",
                                            "wrap": True
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "電話",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": user.phone,
                                            "flex": 5,
                                            "size": "sm",
                                            "color": "#666666",
                                            "wrap": True
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "日期",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": info.bk_date+' '+info.bk_st,
                                            "flex": 5,
                                            "size": "sm",
                                            "color": "#666666",
                                            "wrap": True
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "備註",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": info.bk_ps,
                                            "flex": 5,
                                            "size": "sm",
                                            "color": "#666666",
                                            "wrap": True
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
            }
        }

        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # push message to one user

        #line_bot_api.push_message('U5ee811f1f2f899eb66844500ef14a371', TextSendMessage(text='1'))
        line_bot_api.push_message('U5ee811f1f2f899eb66844500ef14a371', FlexSendMessage(
            alt_text="hello", contents=flex))
        line_bot_api.push_message('Uf7e1093512c0dac60f60974ff53e4a2c', FlexSendMessage(
            alt_text="hello", contents=flex))

        return 'success'
    except Exception as e:
        print(e)
        return 'failure'
