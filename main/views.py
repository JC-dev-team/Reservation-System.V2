from common.utility.recaptcha import check_recaptcha
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .models import BkList, Account, Production, Staff, Store, StoreEvent
from common.serializers import Acc_Serializer,Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from common.serializers import checkAuth, check_bklist, applymember, Store_form_serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from common.utility import auth
from django.db import transaction, DatabaseError
from django.views.decorators.http import require_http_methods
from django.db.models import Q  # complex lookup
from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage
    
# Create your views here.
def preview(request):
    return render(request, 'preview_page.html')

def error(request):
    return render(request, 'error/error.html',{'action':'/preview/'})

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