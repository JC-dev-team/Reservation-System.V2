from datetime import datetime
from django.shortcuts import render, redirect, reverse
from booking.models import ActionLog, BkList, Account, Production, Staff, Store, StoreEvent
from common.serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, \
    Prod_Serializer, Staff_Serializer, Store_Serializer, StoreEvent_Serializer
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
from django.db import transaction, DatabaseError
from django.db.models import Q  # complex lookup
from django.views.decorators.http import require_http_methods


def error(request):
    return render(request, 'error/error.html', {'action': '/softwayliving/login/'})

# admin dashboard ------------------- page


def staff_login_portal(request):
    return render(request, 'admin_login.html')


def staff_check_reservation_page(request):
    return render(request, 'admin_checkreservation.html')


def staff_reservation_page(request):
    return render(request, 'admin_reservation.html')


# function --------------------------
@require_http_methods(['POST', 'GET'])
def staff_auth(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)

        # Check data format
        valid = checkStaffAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.StaffAuthentication(social_id, social_app)

        if result == None or result == False:
            return render(request, 'error/error404.html', {'action': '/softwayliving/login/'})

        elif type(result) == dict:  # error occurred
            return render(request, 'error/error.html', {'error': result['error'], 'action': '/softwayliving/login/'})
        else:
            return render(request, 'admin_dashbroad.html', {'data': result})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e, 'action': '/softwayliving/login/'})


# Ajax API
@require_http_methods(['POST'])
def staff_check_reservation(request):
    try:
        store_id = request.POST.get('store_id', None)
        start_month = request.POST.get('start_month', None)
        end_month = request.POST.get('end_month', None)

        start_month = datetime.strptime(start_month, '%Y-%m-%d').date()
        end_month = datetime.strptime(end_month, '%Y-%m-%d').date()

        bk_queryset = BkList.objects.filter(  # get all available reservation
            store_id=store_id,
            bk_date__range=(start_month, end_month),
            is_cancel=False,
        ).order_by('waiting_num', 'bk_date',  'bk_st')
        # order by will be slow, I think better way is regroup

        # add day off data
        event_queryset = StoreEvent.objects.filter(
            store_id=store_id,
            event_date__range=(start_month, end_month),
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
        return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])
def staff_approval_reservation(request):
    try:
        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)
        with transaction.atomic():  # transaction
            bk_queryset = BkList.objects.select_for_update().filter(
                bk_uuid=bk_uuid,
                bk_date=bk_date,
                is_cancel=False,
                is_confirm=False,
            )
            bk_queryset.update(waiting_num=0, is_confirm=True)
            return JsonResponse({'result': 'success'})

    except BkList.DoesNotExist:
        return JsonResponse({'alert': '資料不存在或是已被刪除'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})


# @require_http_methods(['POST'])
# def staff_add_reservation(request):  # Help client to add reservation
#     try:
#         pass
#     except Exception as e:
#         return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])
def staff_cancel_reservation(request):
    try:
        bk_uuid = request.POST.get('bk_uuid', None)
        bk_date = request.POST.get('bk_date', None)

        with transaction.atomic():  # transaction
            bk_queryset = BkList.objects.select_for_update().filter(
                bk_uuid=bk_uuid,
                bk_date=bk_date,
                is_cancel=False,
            )
            bk_queryset.update(is_cancel=True)
            return JsonResponse({'result': 'success'})

    except BkList.DoesNotExist:
        return JsonResponse({'alert': '資料不存在或是已被刪除'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])  # when there are two time sessions
def staff_add_event(request):  # add rest day as booking
    try:
        store_id = request.POST.get('store_id', None)
        event_date = request.POST.get('event_date', None)
        time_session = request.POST.get('time_session', None)
        event_type = request.POST.get('event_type', None)
        print('time_session1 : ', time_session)
        check data format
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
        print('time_session2 : ', time_session)
        if time_session == 'Allday':
            time_session_arr = ['Lunch', 'Dinner']
        else:
            time_session_arr = [time_session]

        
        with transaction.atomic():  # transaction
            # Check is there same event
            flag = 0
            print('time_session_arr :',time_session_arr)
            for i in time_session_arr:
                event_check = StoreEvent.objects.select_for_update().filter(
                    store_id=store_id,
                    event_date=event_date,
                    time_session=i,
                    event_type=event_type
                ).exists()
                print('event_check : ',event_check)
                print('time_session : ',time_session)
                print('flag :',flag)
                if event_check == False:
                    print('1')
                    queryset = StoreEvent.objects.create(
                        store_id=store_id,
                        event_date=event_date,
                        time_session=i,
                        event_type=event_type
                    )

                elif event_check and time_session == 'Allday' and flag == 0:
                    print('2')
                    flag += 1
                elif event_check and flag == 1:
                    print('3')
                    return JsonResponse({'alert': '全天已經是店休了'})
                else:
                    print('4')
                    return JsonResponse({'alert': '此時段已經是店休了'})

        return JsonResponse({'result': 'success'})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})
