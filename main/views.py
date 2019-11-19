from common.utility.recaptcha import check_recaptcha
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .models import (BkList, Account, Production, Staff, Store, StoreEvent,StaffActionLog,UserActionLog)
from common.serializers import (Acc_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer,UserActionLog_Serializer,StaffActionLog_Serializer)

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

    
# Create your views here.
def preview(request):
    return render(request, 'preview_page.html')

def error(request):
    return render(request, 'error/error.html',{'action':'/preview/'})
