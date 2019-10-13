from datetime import datetime
from django.shortcuts import render, redirect, reverse
from booking.models import ActionLog, BkList, Account, Production, Staff, Store
from common.serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from common.serializers import checkAuth
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
from django.db.models import Q  # complex lookup

def error(request):
    return render(request, 'error/error.html')

# @require_http_methods(['POST','GET'])
# def reservation_login(request):
#     social_id = request.POST.get('social_id', None)
#     social_app = request.POST.get('social_app', None)


@require_http_methods(['POST','GET'])
def check_reservation(request):
    try:
        store_id = request.POST.get('store_id', None)
        # bk_date = request.POST.get('bk_date',None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 資料格式錯誤')
        
        result = auth.ClientAuthentication(
            social_id, social_app)
        if result == None or result == False:  # Using PC or No social login # Account Not Exist
            return redirect('/booking/login/',)
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error.html', {'error': result['error']})
        # Account Exist

        acc_queryset = Account.objects.only('user_id').get(
            social_id=social_id,
            social_app=social_app,
        )
        bk_queryset = BkList.objects.filter(
            user_id=acc_queryset.user_id,
            store_id=store_id,
        )
        store_queryset = Store.objects.get(
            store_id=store_id,
        )
        

        acc_serializer = Acc_Serializer(acc_queryset)
        bk_serializer=Bklist_Serializer(bk_queryset)
        store_serializer=Store_Serializer(store_queryset)
        return render(request, 'check_reservation.html', {
            'data': bk_serializer.data,
            'user_info': acc_serializer.data,
            'store':store_serializer.data,
            })
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})

@require_http_methods(['POST'])
def remove_reservation(request):
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        

        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 資料格式錯誤')
        
        result = auth.ClientAuthentication(
            social_id, social_app)
        if result == None or result == False:  # Using PC or No social login # Account Not Exist
            return redirect('/booking/login/',)
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error.html', {'error': result['error']})
        # Account Exist





    except Exception as e:
        return render(request, 'error/error.html', {'error': e})

