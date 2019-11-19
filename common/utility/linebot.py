from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage


def linebot_send_msg(line_id, user=None,info=None):
    try:
        if info['time_session'] == "Dinner":
            time_session_info = '晚餐'
        else:
            time_session_info = '午餐'

        if info['is_confirm'] :
            is_confirm_info ='SoftWay 訂位已確認'
            color = '#05C11C'
        elif info['is_cancel']:
            is_confirm_info ='SoftWay 訂位已取消'
            color = '#E83B4F'
        else :
            is_confirm_info ='SoftWay 訂位處理中'
            color = '#E7881D'

        if info['bk_ps']== None or info['bk_ps']== '':
            ps_info = '無'
        else:
            ps_info = info['bk_ps']

        username_info = user['username']+' '+str(info['adult'])+'大'+str(info['children'])+'小'
        date_info = str(info['bk_date'])+' '+time_session_info+' '+str(info['bk_st'])
        phone_info = user['phone']
        habit_info = info['bk_habit']
        price_info = str(info['bk_price'])
        
        
        text = ""
        flex ={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": is_confirm_info,
                            "size": "xl",
                            "weight": "bold",
                            "color": color
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
                                            "text": username_info,
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
                                            "text": phone_info,
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
                                            "text":date_info,
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
                                            "text": "價位",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": 'NT$ ' + price_info,
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
                                            "text": "習慣",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        },
                                        {
                                            "type": "text",
                                            "text": habit_info,
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
                                            "text": ps_info,
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
        line_bot_api.push_message('U5ee811f1f2f899eb66844500ef14a371', FlexSendMessage(
            alt_text="訂位資訊通知", contents=flex))
        # push message to one user
        line_bot_api.push_message('Uf7e1093512c0dac60f60974ff53e4a2c', FlexSendMessage(
            alt_text="訂位資訊通知", contents=flex))

        return 'success'
    except Exception as e:
        return 'failure'
