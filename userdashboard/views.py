from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect, reverse
from main.models import (BkList, Account, Production,
                         Staff, Store, StoreEvent, StaffActionLog, UserActionLog)
from common.serializers import (Acc_Serializer, Bklist_Serializer, Prod_Serializer,
                                Staff_Serializer, Store_Serializer, UserActionLog_Serializer, StaffActionLog_Serializer)
from common.serializers import checkAuth, Store_form_serializer
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
from django.conf import settings
from common.utility.auth import _login_required as Clinet_login_required
from common.utility.geolocation import get_client_ip
from common.utility.linebot import linebot_send_msg

def error(request):
    request.session.flush()
    return render(request, 'error/error.html', {'action': '/userdashboard/login/'})


@require_http_methods(['GET'])
def user_login(request):
    return render(request, 'user_login.html')


@require_http_methods(['POST', 'GET'])
def user_auth(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        social_name = request.POST.get('social_name', None)

        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.ClientAuthentication(social_id, social_app)

        if result == None:
            request.session.flush()
            return render(request, 'error/error404.html', {'action': '/userdashboard/login/'})
        elif result == False:
            request.session['social_id'] = social_id
            request.session['social_app'] = social_app
            request.session['social_name'] = social_name
            return render(request, 'member.html', {'google_keys': settings.RECAPTCHA_PUBLIC_KEY})

        elif type(result) == dict:  # error occurred
            request.session.flush()
            return render(request, 'error/error.html', {'error': result['error'], 'action': '/userdashboard/login/'})
        else:
            if 'is_Login' in request.session:
                request.session.flush()
            request.session['is_Login'] = True
            request.session['social_id'] = social_id
            request.session['social_app'] = social_app
            request.session['social_name'] = social_name
            request.session['user_id'] = result.user_id
            with transaction.atomic():  # transaction
                try:
                    ip,location,err=get_client_ip(request)
                    if err != None:
                        raise Exception(err)
                        # return render(request, 'error/error.html', {'error': str(err), 'action': '/softwayliving/login/'})
                    UserActionLog.objects.create(
                        user_id=result.user_id,
                        location=location, 
                        ip=ip,
                        operation='Login'
                    )
                except Exception as e:
                    pass
            return render(request, 'user_dashboard.html', {'data': result})
    except Exception as e:
        request.session.flush()

        return render(request, 'error/error.html', {'error': '發生未知錯誤', 'action': '/userdashboard/login/'})


@require_http_methods(['POST', 'GET'])
@Clinet_login_required(redirect_url='/userdashboard/login/')
def user_check_reservation(request):
    try:
        if request.session.get('is_Login', False) == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/userdashboard/login/'})

        request.session.set_expiry(900)
        user_id = request.session.get('user_id', None)
        # Account Exist Check
        acc_queryset = Account.objects.get(
            user_id=user_id
        )
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        bk_queryset = BkList.objects.filter(
            user_id=user_id,
            bk_date__gte=now,
            is_cancel=False,

        ).order_by('is_confirm', '-waiting_num', 'bk_date', 'bk_st')
        # If data not exists
        if bk_queryset.exists() == False:
            account_serializer = Acc_Serializer(acc_queryset)
            return render(request, 'user_checkreservation.html', {
                'data': False,
                'user_info': account_serializer.data,
            })

        store_arr = []  # store data array
        for i in bk_queryset:
            store_queryset = Store.objects.only('store_id', 'store_name', 'store_address', 'store_phone').get(
                store_id=i.store_id
            )

            store_serializer = Store_form_serializer(store_queryset)
            store_arr.append(store_serializer.data)

        account_serializer = Acc_Serializer(acc_queryset)
        bk_serializer = Bklist_Serializer(bk_queryset, many=True)
        return render(request, 'user_checkreservation.html', {
            'data': bk_serializer.data,
            'user_info': account_serializer.data,
            'store': store_arr,
        })
    except Account.DoesNotExist:  # Account Not Exist
        request.session.flush()
        return render(request, 'error/error.html', {'error': '帳號不存在', 'action': '/userdashboard/login/'})
    except Exception as e:

        request.session.flush()
        return render(request, 'error/error.html', {'error': '發生未知錯誤', 'action': '/userdashboard/login/'})


# Ajax API
@require_http_methods(['POST'])
@Clinet_login_required(redirect_url='/userdashboard/login/')
def user_cancel_reservation(request):
    try:
        if request.session.get('is_Login', False) == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/userdashboard/login/'})
        # use session catch
        request.session.set_expiry(900)

        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)
        social_id = request.session.get('social_id', None)
        # Account Exist
        with transaction.atomic():  # transaction
            bk_date_ = datetime.strptime(bk_date, '%Y-%m-%d')
            bk_date_tmp = bk_date_ - timedelta(days=3)
            if bk_date_tmp < datetime.now():
                return JsonResponse({'alert': '超過三天取消訂位期限'})
            else:
                bk_date_ = bk_date_.date()  # format datetime
                bk_queryset = BkList.objects.select_for_update().get(
                    bk_uuid=bk_uuid,
                    bk_date=bk_date,
                    is_cancel=False,
                )
                bk_queryset.is_cancel = True
                bk_queryset.save()
                bklist_serializer = Bklist_Serializer(bk_queryset)
                acc_queryset=Account.objects.get(
                    user_id=bk_queryset.user_id
                )
                account_serializer = Acc_Serializer(acc_queryset)
                # Use linebot
                line_send_result = linebot_send_msg(
                    social_id, account_serializer.data, bklist_serializer.data)
                
                return JsonResponse({'result': 'success'})
    except BkList.DoesNotExist:
        return JsonResponse({'error': '資料已經刪除或是不存在', 'action': '/userdashboard/error/'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/userdashboard/error/'})
