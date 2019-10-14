from datetime import datetime, date
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
from django.views.decorators.http import require_http_methods
from datetime import datetime


def error(request):
    return render(request, 'error/error.html', {'action': '/userdashboard/login/'})


@require_http_methods(['POST', 'GET'])
def user_login(request):
    return render(request, 'user_login.html')


@require_http_methods(['POST', 'GET'])
def user_auth(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)

        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.ClientAuthentication(social_id, social_app)

        if result == None or result == False:
            return render(request, 'error/error404.html', {'action': '/userdashboard/login/'})

        elif type(result) == dict:  # error occurred
            return render(request, 'error/error.html', {'error': result['error'], 'action': '/userdashboard/login/'})
        else:
            return render(request, 'user_dashboard.html', {'data': result})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e, 'action': '/userdashboard/login/'})


@require_http_methods(['POST', 'GET'])
def user_check_reservation(request):
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
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.ClientAuthentication(
            social_id, social_app)
        print(result)
        print('hello')
        if result == None or result == False:  # Using PC or No social login # Account Not Exist
            return redirect('/userdashboard/login/',)
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error_check.html', {'error': result['error'], 'action': '/userdashboard/login/'})
        # Account Exist
        print('hello1')
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')

        acc_queryset = Account.objects.only('user_id').get(
            social_id=social_id,
            social_app=social_app,
        )
        bk_queryset = BkList.objects.filter(
            user_id=acc_queryset.user_id,
            store_id=store_id,
            bk_date__gte=now,
        )
        store_queryset = Store.objects.get(
            store_id=store_id,
        )

        acc_serializer = Acc_Serializer(acc_queryset)
        bk_serializer = Bklist_Serializer(bk_queryset)
        store_serializer = Store_Serializer(store_queryset)

        return render(request, 'user_check_reservation.html', {
            'data': bk_serializer.data,
            'user_info': acc_serializer.data,
            'store': store_serializer.data,
        })
    except Exception as e:
        return render(request, 'error/error.html', {'error': e, 'action': '/userdashboard/login/'})


# Ajax API
@require_http_methods(['POST'])
def user_remove_reservation(request):
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)

        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')
        
        result = auth.ClientAuthentication(
            social_id, social_app)
  
        if result == None or result == False:  # Using PC or No social login # Account Not Exist
            return redirect('/userdashboard/login/',)
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            raise Exception('error')
        # Account Exist
       
        with transaction.atomic():  # transaction
            bk_date_ = datetime.strptime(bk_date, '%Y-%m-%d')
            bk_date_tmp = bk_date_ - datetime.timedelta(days=3)

            if bk_date_tmp > datetime.datetime.now():
                return JsonResponse({'error': '超過三天取消訂位期限'})
            else:
                bk_date_ = bk_date_.date()  # format datetime
                bk_queryset = BkList.objects.select_for_update().get(
                    bk_uuid=bk_uuid,
                    is_cancel=False,
                )

                bk_queryset.update(is_cancel=True)
                return JsonResponse({'result': True})

    except BkList.DoesNotExist:
        return JsonResponse({'error': '資料已經刪除'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})
