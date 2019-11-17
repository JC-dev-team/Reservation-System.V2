from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect, reverse
from main.models import BkList, Account, Production, Staff, Store, StoreEvent
from common.serializers import Acc_Serializer, Bklist_Serializer, \
    Prod_Serializer, Staff_Serializer, Store_Serializer, StoreEvent_Serializer, Store_form_serializer
from common.serializers import checkStaffAuth
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from common.utility import auth
from common.utility.auth import _login_required
from django.contrib.auth import authenticate,  logout
from django.contrib.auth import login as auth_login
from django.db import transaction, DatabaseError
from django.db.models import Q  # complex lookup
from django.views.decorators.http import require_http_methods
from django.contrib.sessions.models import Session
from django.conf import settings
from common.utility.recaptcha import check_recaptcha
from django.contrib.auth.decorators import login_required
from common.utility.linebot import linebot_send_msg
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy


def error(request):
    request.session.flush()
    return render(request, 'error/error.html', {'action': '/softwayliving/login/'})

# admin dashboard ------------------- page


def staff_login_portal(request):
    # If the session is not outdated
    if request.user.is_authenticated:
        return render(request, 'admin_dashbroad.html')
    return render(request, 'admin_login.html', {'error': ''})


@login_required(login_url='/softwayliving/login/')
def staff_check_reservation_page(request):
    request.session.set_expiry(900)
    return render(request, 'admin_checkreservation.html')


@login_required(login_url='/softwayliving/login/')
def staff_reservation_page(request):
    request.session.set_expiry(900)
    return render(request, 'admin_reservation.html',)

# function --------------------------
@require_http_methods(['GET'])
@login_required(login_url='/softwayliving/login/')
def member_management(request):
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        queryset = Account.objects.filter(is_active=True)
        serializer_class = Acc_Serializer(queryset, many=True)
        return render(request, 'admin_memberlist.html', {'data': serializer_class.data})
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


@require_http_methods(['POST', 'GET'])
def staff_auth(request):  # authentication staff
    try:
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if int(request.session.get('try_time', 0)) >= 5:
            return render(request, 'error/error.html',
                          {
                              'action': '/softwayliving/login/',
                              'error': 'Trying too many times',
                          })

        # Check Auth
        result = auth.StaffAuthentication(email, password)
        if result == None or result == False:
            request.session.flush()
            return render(request, 'error/error404.html', {'action': '/softwayliving/login/'})
        elif result == 'ERROR':
            request.session['try_time'] = int(
                request.session.get('try_time', 0))+1
            return render(request, 'admin_login.html', {'error': '帳號或是密碼輸入錯誤'})
        elif type(result) == dict:  # error occurred
            request.session.flush()
            return render(request, 'error/error.html', {'error': result['error'], 'action': '/softwayliving/login/'})
        else:
            if request.user.is_authenticated:
                request.session.flush()

            if result['is_active'] == False:
                return render(request, 'error/error.html', {'error': '很抱歉，帳號遭到鎖定，請洽客服人員', 'action': '/softwayliving/login/'})

            staff = authenticate(request, email=email, password=password)
            auth_login(request, staff,
                       backend='common.utility.auth.StaffAuthBackend')
            request.session['is_Login'] = True
            request.session['store_id'] = result['store']
            request.session['staff_id'] = result['staff_id']
            request.session['staff_name'] = result['staff_name']

            return render(request, 'admin_dashbroad.html')
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


@require_http_methods(['POST'])
@login_required(login_url='/softwayliving/login/')
@check_recaptcha
def staff_add_reservation(request):  # Help client to add reservation
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        phone = request.POST.get('phone', None)
        username = request.POST.get('username', None)
        if len(phone) != 10:
            return redirect('/softwayliving/reservation/')
        try:
            queryset = Account.objects.get(
                phone=phone,
            )
        except Account.DoesNotExist:
            with transaction.atomic():  # transaction
                acc = Account.objects.create(
                    phone=phone,
                    username=username,
                    social_id='電話訂位',
                    social_app='電話訂位',
                    social_name='電話訂位',
                    is_active=True,
                )
                queryset = Account.objects.get(
                    phone=phone,
                    username=username,
                )
        except Account.MultipleObjectsReturned:
            return render(request, 'admin_reservation.html', {'error': '姓名與手機重複申請，無法進行訂位與註冊'})

        request.session['user_id'] = queryset.user_id

        serializer_class = Acc_Serializer(queryset)
        return render(request, 'reservation.html', {
            'data': serializer_class.data,
            'google_keys': settings.RECAPTCHA_PUBLIC_KEY})

    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


@require_http_methods(['POST'])
@login_required(login_url='/softwayliving/login/')
@check_recaptcha
def admin_InsertReservation(request):  # insert booking list
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        # For validation
        staff_id = request.session.get('staff_id', None)
        is_Login = request.session.get('is_Login', None)

        # Check staff is login
        if is_Login != True or staff_id == None:
            return redirect('/softwayliving/login/',)
        # staff account Exist
        # insert data
        store_id = request.session.get('store_id', None)
        user_id = request.session.get('user_id', None)
        bk_date = request.POST.get('bk_date', None)
        bk_st = request.POST.get('bk_st', None)
        adult = request.POST.get('adult', None)
        children = request.POST.get('children', None)
        bk_habit = request.POST.get('bk_habit', None)
        event_type = request.POST.get('event_type', None)
        time_session = request.POST.get('time_session', None)
        entire_time = request.POST.get('entire_time', False)
        bk_price = request.POST.get('price', None)
        is_cancel = False
        waiting_num = 0
        is_confirm = False
        # Check data format
        Bklist_Serializer(data={
            'user_id': user_id,
            'store_id': store_id,
            'bk_st': bk_st,
            'adult': adult,
            'children': children,
            'bk_habit': bk_habit,
            'event_type': event_type,
            'time_session': time_session,
            'entire_time': entire_time,
            'bk_price': bk_price,
            'is_cancel': is_cancel,
            'waiting_num': waiting_num,
            'is_confirm': is_confirm,

        })
        # ---------------------------------
        total = int(adult)+int(children)
        exact_seat = 0
        # modify insert data
        if time_session == 'D':
            time_session = 'Dinner'
        elif time_session == 'L':
            time_session = 'Lunch'
        else:
            raise Exception('資料輸入時，發生錯誤')

        with transaction.atomic():  # transaction
            # get the store seat
            store_query = Store.objects.only('seat').select_for_update().get(
                store_id=store_id
            )

            # get the booking event of that time session
            bk_queryset = BkList.objects.select_for_update().filter(
                store_id=store_id,
                bk_date=bk_date,
                time_session=time_session,
                is_cancel=is_cancel,
                waiting_num=0,
            )

            # count is that enough for seat values
            for i in bk_queryset:
                number = int(i.adult)+int(i.children)
                exact_seat += number

            # get waiting_num
            if (exact_seat+total) > store_query.seat:  # need waiting
                waiting_num = BkList.objects.only('waiting_num').select_for_update().filter(
                    store_id=store_id,
                    bk_date=bk_date,
                    time_session=time_session,
                    is_cancel=is_cancel,
                    waiting_num__gt=0,
                ).count()
                waiting_num += 1
            else:  # don't need to wait
                waiting_num = 0

            final_queryset = BkList.objects.create(  # insert data
                user_id=user_id,
                store_id=store_id,
                bk_date=bk_date,
                bk_st=bk_st,
                adult=adult,
                children=children,
                bk_habit=bk_habit,
                event_type=event_type,
                time_session=time_session,
                entire_time=entire_time,
                is_cancel=is_cancel,
                waiting_num=waiting_num,
                bk_price=bk_price,
                is_confirm=is_confirm,
            )
            get_user_info = Account.objects.only('user_id', 'social_id', 'username').get(
                user_id=user_id,
            )

            get_store_name = Store.objects.only(
                'store_id',
                'store_name',
                'store_address',
                'store_phone',).get(
                store_id=store_id
            )

            if final_queryset.time_session == 'Dinner':
                final_queryset.time_session = '晚餐'
            else:
                final_queryset.time_session = '午餐'

            account_serializer = Acc_Serializer(get_user_info)
            store_serializer = Store_form_serializer(get_store_name)
            bklist_serializer = Bklist_Serializer(final_queryset)

            line_send_result = linebot_send_msg(
                get_user_info.social_id, account_serializer.data, bklist_serializer.data)

            if line_send_result == 'failure':
                raise Exception('linebot send message failed')
            del request.session['user_id']
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return render(request, 'reservation_finish.html', {
                'data': bklist_serializer.data,
                'store': store_serializer.data,
                'user_info': account_serializer.data,
                'action': 'admin'})
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


@login_required(login_url='/softwayliving/login/')
def staff_productions_page(request):
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        queryset = Production.objects.filter(
            store_id=store_id).order_by('prod_price')
        serializers = Prod_Serializer(queryset, many=True)

        return render(request, 'admin_productlist.html', {'data': serializers.data})
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


@login_required(login_url='/softwayliving/login/')
def staff_admins_page(request):
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)

        queryset = Staff.objects.filter(
            store_id=store_id
        ).order_by('-staff_level')
        serializers = Staff_Serializer(queryset, many=True)

        return render(request, '', {'data': serializers.data})
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})

@login_required(login_url='/softwayliving/login/')
def staff_stores_page(request):
    try:
        if request.user.is_authenticated == False:
            return render(request, 'error/error.html', {'error': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)

        queryset = Store.objects.filter(
            store_id=store_id
        ).order_by('-staff_level')
        serializers = Store_Serializer(queryset, many=True)

        return render(request, '', {'data': serializers.data})
    except Exception as e:
        request.session.flush()
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


# Ajax API ---------------------------------------------
@require_http_methods(['POST'])
def staff_check_reservation(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'alert': 'Not Valid 請先登入'})
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        bk_queryset = BkList.objects.filter(  # get all available reservation
            store_id=store_id,
            bk_date__gte=now,
            is_cancel=False,
        ).order_by('-is_confirm', 'waiting_num', 'bk_date',  'bk_st')
        # order by will be slow, I think better way is regroup

        # add day off data
        event_queryset = StoreEvent.objects.filter(
            store_id=store_id,
            event_date__gte=now,
        )
        # get user phone number
        acc_arr = []
        for i in bk_queryset:
            acc_queryset = Account.objects.get(
                user_id=i.user_id,
            )
            acc_serializers = Acc_Serializer(acc_queryset)
            acc_arr.append(acc_serializers.data)

        event_serializers = StoreEvent_Serializer(event_queryset, many=True)
        bk_serializers = Bklist_Serializer(bk_queryset, many=True)
        return JsonResponse({
            'result': bk_serializers.data,
            'event': event_serializers.data,
            'account': acc_arr,
        })

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_confirm_reservation(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)
        bk_ps = request.POST.get('bk_ps', None)
        with transaction.atomic():  # transaction
            bk_queryset = BkList.objects.select_for_update().filter(
                bk_uuid=bk_uuid,
                bk_date=bk_date,
                is_cancel=False,
                is_confirm=False,
            )

            if bk_queryset.exists() == False:
                return JsonResponse({'alert': '資料已經被刪除或是訂位完成'})

            bk_queryset.update(waiting_num=0, is_confirm=True, bk_ps=bk_ps)

            bklist_queryset = BkList.objects.select_for_update().get(
                bk_uuid=bk_uuid,
            )

            acc_queryset = Account.objects.get(
                user_id=bklist_queryset.user_id
            )
            bk_serializer = Bklist_Serializer(bklist_queryset)
            acc_serializer = Acc_Serializer(acc_queryset)
            line_send_result = linebot_send_msg(
                acc_queryset.social_id, acc_serializer.data, bk_serializer.data)

            if line_send_result == 'failure':
                raise Exception('linebot send message failed')
            return JsonResponse({'result': 'success'})

    except Account.DoesNotExist:
        return JsonResponse({'alert': '客戶資料不存在'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_pass_reservation(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        bk_uuid = request.POST.get('bk_uuid', None)
        time_session = request.POST.get('time_session', None)
        bk_date = request.POST.get('bk_date', None)
        bk_ps = request.POST.get('bk_ps', None)
        store_id = request.session.get('store_id', None)

        with transaction.atomic():  # transaction
            store_queryset = Store.objects.only('seat').get(store_id=store_id,)
            queryset = BkList.objects.select_for_update().filter(
                bk_date=bk_date,
                is_cancel=False,
                time_session=time_session,
            )
            # Must be only one data
            bk_queryset = queryset.filter(
                bk_uuid=bk_uuid, is_confirm=False,)
            if bk_queryset.exists() == False:
                return JsonResponse({'alert': '資料已經被刪除或是訂位完成'})
            # Get total number of guests
            total = int(bk_queryset[0].adult) + int(bk_queryset[0].children)

            # Get the list before the bk_queryset waiting_num=0
            beforelist = queryset.filter(
                waiting_num=0,
            )
            for i in beforelist:
                total += int(i.adult)+int(i.children)
            if total > store_queryset.seat:
                return JsonResponse({'alert': '請先刪除前面非候補訂位'})
            bk_queryset.update(waiting_num=0, is_confirm=True, bk_ps=bk_ps)
            bklist_serializer = bklist_serializer(bk_queryset)
            acc_queryset = Account.objects.get(
                user_id=bk_queryset.user_id
            )

            line_send_result = linebot_send_msg(
                acc_queryset.social_id, acc_queryset, bklist_serializer.data)

            if line_send_result == 'failure':
                raise Exception('linebot send message failed')

            return JsonResponse({'result': 'success'})

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_cancel_reservation(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)

        with transaction.atomic():  # transaction
            bk_queryset = BkList.objects.select_for_update().filter(
                bk_uuid=bk_uuid,
                bk_date=bk_date,
                is_cancel=False,
            )
            if bk_queryset.exists() == False:
                return JsonResponse({'alert': '資料不存在或是已被刪除'})
            bk_queryset.update(is_cancel=True)
            return JsonResponse({'result': 'success'})

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])  # when there are two time sessions
def staff_add_event(request):  # add rest day as booking
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})

        event_date = request.POST.get('event_date', None)
        time_session = request.POST.get('time_session', None)
        event_type = request.POST.get('event_type', None)
        # check data format
        valid = StoreEvent_Serializer(
            data={
                'store': store_id,
                'event_date': event_date,
                'time_session': time_session,
                'event_type': event_type
            }
        )
        if valid.is_valid() == False:
            return JsonResponse({'error': 'Not valid, 輸入資料格式錯誤'})
        if time_session == 'Allday':
            time_session_arr = ['Lunch', 'Dinner']
        else:
            time_session_arr = [time_session]

        with transaction.atomic():  # transaction
            # Check is there same time session
            flag = 0
            for i in time_session_arr:
                event_check = StoreEvent.objects.select_for_update().filter(
                    store_id=store_id,
                    event_date=event_date,
                    time_session=i,
                    event_type=event_type
                ).exists()
                if event_check == False:
                    queryset = StoreEvent.objects.create(
                        store_id=store_id,
                        event_date=event_date,
                        time_session=i,
                        event_type=event_type
                    )

                elif event_check and time_session == 'Allday' and flag == 0:
                    flag += 1
                elif event_check and flag == 1:
                    return JsonResponse({'alert': '全天已經是店休了'})
                else:
                    return JsonResponse({'alert': '此時段已經是店休了'})

            return JsonResponse({'result': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})

# AJAX checklist
@require_http_methods(['GET'])
def staff_not_confirmed(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        # Get now
        store_id = request.session.get('store_id', None)

        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})

        today = date.today()
        now = today.strftime('%Y-%m-%d')
        bk_queryset = BkList.objects.filter(
            is_confirm=False,
            is_cancel=False,
            bk_date__gte=now,
            store_id=store_id,
        )
        # get user phone number
        acc_arr = []
        for i in bk_queryset:

            acc_queryset = Account.objects.get(
                user_id=i.user_id,
            )
            acc_serializers = Acc_Serializer(acc_queryset)
            acc_arr.append(acc_serializers.data)

        bk_serializers = Bklist_Serializer(bk_queryset, many=True)
        return JsonResponse({
            'result': bk_serializers.data,
            'account': acc_arr,
        })
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['GET'])
def staff_is_confirmed(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        queryset = BkList.objects.filter(
            is_confirm=True,
            is_cancel=False,
            bk_date__gte=now,
            store_id=store_id,
        )
        acc_arr = []
        for i in queryset:

            acc_queryset = Account.objects.get(
                user_id=i.user_id,
            )
            acc_serializers = Acc_Serializer(acc_queryset)
            acc_arr.append(acc_serializers.data)
        bk_serializers = Bklist_Serializer(queryset, many=True)
        return JsonResponse({
            'result': bk_serializers.data,
            'account': acc_arr,
        })
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['GET'])
def staff_is_cancel(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        queryset = BkList.objects.filter(
            is_cancel=True,
            bk_date__gte=now,
            store_id=store_id,
        )
        acc_arr = []
        for i in queryset:

            acc_queryset = Account.objects.get(
                user_id=i.user_id,
            )
            acc_serializers = Acc_Serializer(acc_queryset)
            acc_arr.append(acc_serializers.data)
        bk_serializers = Bklist_Serializer(queryset, many=True)
        return JsonResponse({
            'result': bk_serializers.data,
            'account': acc_arr,
        })
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['GET'])
def staff_is_waiting(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})
        # Get now
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        queryset = BkList.objects.filter(
            is_cancel=False,
            bk_date__gte=now,
            waiting_num__gt=0,
            is_confirm=False,
            store_id=store_id,

        )
        acc_arr = []
        for i in queryset:

            acc_queryset = Account.objects.get(
                user_id=i.user_id,
            )
            acc_serializers = Acc_Serializer(acc_queryset)
            acc_arr.append(acc_serializers.data)
        bk_serializers = Bklist_Serializer(queryset, many=True)
        return JsonResponse({
            'result': bk_serializers.data,
            'account': acc_arr,
        })
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_modify_member(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)
        # Set auth in future
        user_id = request.POST.get('user_id', None)
        birth = request.POST.get('birth', None)
        username = request.POST.get('username', None)
        phone = request.POST.get('phone', None)
        with transaction.atomic():  # transaction
            try:
                queryset = Account.objects.get(user_id=user_id)
                if birth != None and birth != '' and birth != 'None':
                    queryset.birth = birth
                queryset.username = username
                queryset.phone = phone
                queryset.save()
                return JsonResponse({'result': 'success'})
            except Account.DoesNotExist:
                return JsonResponse({'alert': '帳號已刪除或是不存在'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_lock_member(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})

        request.session.set_expiry(900)
        # Set auth in future
        is_Login = request.session.get('is_Login', None)
        staff_id = request.session.get('staff_id', None)
        if is_Login != True or staff_id == None:
            return JsonResponse({'alert': 'Not Valid, 請登入帳號'})

        user_id = request.POST.get('user_id', None)
        with transaction.atomic():  # transaction
            try:
                queryset = Account.objects.get(user_id=user_id)
                queryset.is_active = False
                queryset.save()
                return JsonResponse({'result': 'success'})
            except Account.DoesNotExist:
                return JsonResponse({'alert': '帳號已刪除或是不存在'})

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def staff_cancel_event(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        request.session.set_expiry(900)

        store_id = request.session.get('store_id', None)
        if store_id == None:
            return JsonResponse({'error': 'Not valid, 請先登入'})

        event_date = request.POST.get('event_date', None)
        time_session = request.POST.get('time_session', None)
        event_type = request.POST.get('event_type', None)

        with transaction.atomic():  # transaction
            try:
                instance = StoreEvent.objects.get(
                    store_id=store_id,
                    event_date=event_date,
                    time_session=time_session,
                    event_type=event_type,
                )
                instance.delete()
            except StoreEvent.DoesNotExist:
                return JsonResponse({'alert': '該事件已刪除或是不存在'})
            return JsonResponse({'result': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def add_admin(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_superuser == False:
            return JsonResponse({'alert': '權限不足'})
        request.session.set_expiry(900)

        store_id = request.POST.get('store_id', None)
        email = request.POST.get('email', None)
        staff_level = request.POST.get('staff_level', None)
        is_superuser = request.POST.get('is_superuser', False)
        is_admin = request.POST.get('is_admin', False)
        staff_name = request.POST.get('staff_name', None)
        password = make_password(request.POST.get('password', None))

        with transaction.atomic():  # transaction
            queryset = Staff.objects.create_admin(
                email=email,
                password=password,
                staff_level=staff_level,
                staff_name=staff_name,
                store_id=store_id,
                is_superuser=is_superuser,
                is_admin=is_admin,
            )
            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def delete_admin(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_superuser == False:
            return JsonResponse({'alert': '權限不足'})

        request.session.set_expiry(900)
        staff_id = request.POST.get('staff_id', None)
        staff_name = request.POST.get('staff_name', None)
        email = request.POST.get('email', None)

        with transaction.atomic():  # transaction
            queryset = Staff.objects.get(
                staff_id=staff_id,
                staff_name=staff_name,
                email=email,
            )
            queryset.delete()

            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def add_product(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_admin == False:
            return JsonResponse({'alert': '權限不足'})

        request.session.set_expiry(900)

        store_id = request.session.get('store_id', None)
        prod_name = request.POST.get('prod_name', None)
        prod_price = request.POST.get('prod_price', None)
        prod_img = request.POST.get('prod_img', None)
        prod_desc = request.POST.get('prod_desc', None)

        with transaction.atomic():  # transaction
            queryset = Production.objects.create(
                store_id=store_id,
                prod_name=prod_name,
                prod_price=prod_price,
                prod_img=prod_img,
                prod_desc=prod_desc,
            )
            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def modify_product(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_admin == False:
            return JsonResponse({'alert': '權限不足'})
        request.session.set_expiry(900)
        prod_id = request.POST.get('prod_id', None)
        store_id = request.session.get('store_id', None)
        prod_name = request.POST.get('prod_name', None)
        prod_price = request.POST.get('prod_price', None)
        prod_img = request.POST.get('prod_img', None)
        prod_desc = request.POST.get('prod_desc', None)

        with transaction.atomic():  # transaction
            queryset = Production.objects.get(
                prod_id=prod_id,
                store_id=store_id,
            )
            queryset.prod_name = prod_name
            queryset.prod_price = prod_price
            queryset.prod_img = prod_img
            queryset.prod_desc = prod_desc
            queryset.save()
            return JsonResponse({'result': 'success'})
    except Production.DoesNotExist:
        return JsonResponse({'alert': '該資料不存在'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def delete_product(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_admin == False:
            return JsonResponse({'alert': '權限不足'})

        request.session.set_expiry(900)
        prod_id = request.POST.get('prod_id', None)
        store_id = request.session.get('store_id', None)
        with transaction.atomic():  # transaction
            queryset = Production.objects.get(
                prod_id=prod_id,
                store_id=store_id
            )
            queryset.delete()
            return JsonResponse({'reuslt': 'success'})
    except Production.DoesNotExist:
        return JsonResponse({'alert': '該資料不存在或是已經被刪除'})

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def add_store(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_superuser == False:
            return JsonResponse({'alert': '權限不足'})
        request.session.set_expiry(900)
        store_name = request.POST.get('store_name', None)
        store_address = request.POST.get('store_address', None)
        store_phone = request.POST.get('store_phone', None)
        store_fax = request.POST.get('store_fax', None)
        tk_service = request.POST.get('tk_service', False)
        seat = request.POST.get('seat', None)

        with transaction.atomic():  # transaction
            queryset = Store.objects.create(
                store_name=store_name,
                store_address=store_address,
                store_phone=store_phone,
                store_fax=store_fax,
                tk_service=tk_service,
                seat=seat,
            )

            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def modify_store(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_superuser == False:
            return JsonResponse({'alert': '權限不足'})

        request.session.set_expiry(900)
        store_id = request.POST.get('store_id', None)
        store_name = request.POST.get('store_name', None)
        store_address = request.POST.get('store_address', None)
        store_phone = request.POST.get('store_phone', None)
        store_fax = request.POST.get('store_fax', None)
        tk_service = request.POST.get('tk_service', False)
        seat = request.POST.get('seat', None)

        with transaction.atomic():  # transaction
            queryset = Store.objects.get(
                store_id=store_id,
            )
            queryset.store_name = store_name
            queryset.store_address = store_address
            queryset.store_phone = store_phone
            queryset.store_fax = store_fax
            queryset.tk_service = tk_service
            queryset.seat = seat
            queryset.save()
            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})


@require_http_methods(['POST'])
def delete_store(request):
    try:
        if request.user.is_authenticated == False:
            return JsonResponse({'outdated': '憑證已經過期，請重新登入', 'action': '/softwayliving/login/'})
        elif request.user.is_superuser == False:
            return JsonResponse({'alert': '權限不足'})

        request.session.set_expiry(900)
        store_id = request.POST.get('store_id', None)
        store_name = request.POST.get('store_name', None)
        with transaction.atomic():  # transaction
            queryset = Store.objects.get(
                store_id=store_id,
                store_name=store_name,
            )
            queryset.delete()

            return JsonResponse({'reuslt': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤', 'action': '/softwayliving/error/'})

# @csrf_exempt
# def event_AAAA(request):
#     store_id = '6f48f753-e4f0-11e9-bfcb-0e9f22d909c0'
#     event_type ='Day off'
#     today = date.today()
#     event_date = deepcopy(today)
#     counter =0
#     while event_date.strftime('%Y-%m-%d')<='2022-12-31':

#         if event_date.weekday()!=0:
#             counter+=1
#             event_date= (today+timedelta(days=counter))
#         else :
#             event_date=event_date.strftime('%Y-%m-%d')
#             with transaction.atomic():  # transaction
#                 StoreEvent.objects.create(
#                     store_id=store_id,
#                     event_type=event_type,
#                     event_date=event_date,
#                     time_session='Lunch')
#                 StoreEvent.objects.create(
#                     store_id=store_id,
#                     event_type=event_type,
#                     event_date=event_date,
#                     time_session='Dinner')
#                 counter+=1
#                 event_date= (today+timedelta(days=counter))

#     return JsonResponse({'reuslt': 'success'})
