from common.utility.recaptcha import check_recaptcha
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .models import ActionLog, BkList, Account, Production, Staff, Store, StoreEvent
from common.serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from common.serializers import checkAuth, check_bklist, applymember
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
# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# ----- Class site ----------------------


# class AccountViewSet(viewsets.ModelViewSet):  # api get account data
#     queryset = Account.objects.all()
#     serializer_class = Acc_Serializer

#     def get_queryset(self):
#         queryset = self.queryset
#         phone = self.request.query_params.get('phone', None)
#         social_id = self.request.query_params.get('social_id', None)

#         query_set = queryset.filter(phone=phone)
#         return query_set

# Definition site ------------------------------------------------
# def error_404_view(request,exception):
#     # data = {"name": "ThePythonDjango.com"}
#     return render(request,'error/error404.html')

@require_http_methods(['POST'])
@check_recaptcha
def ToBookingView(request):  # The member.html via here in oreder to enroll new member
    try:
        phone = request.POST.get('phone', None)
        username = request.POST.get('username', None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        if social_id == None or social_app == None or social_id == '' or social_app == '':
            raise Exception('Not Valid, 無法取得帳號資料')
        # Check data format
        if len(phone) != 10:
            raise Exception('Not Valid, 手機長度有誤')
        valid = applymember(data={
            'social_id': social_id,
            'social_app': social_app,
            'username': username,
            'phone': phone,
        })

        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')
        with transaction.atomic():  # transaction
            queryset = Account.objects.create(
                phone=phone,
                username=username,
                social_id=social_id,
                social_app=social_app,
            )
            queryset = Account.objects.select_for_update().get(
                phone=phone,
                username=username,
                social_id=social_id,
                social_app=social_app
            )

        serializer_class = Acc_Serializer(queryset)
        # render html

        return render(request, 'reservation.html', {
            'data': serializer_class.data,
            'google_keys': settings.RECAPTCHA_PUBLIC_KEY})

    except Exception as e:
        # render html
        return render(request, 'error/error.html', {'error': e, 'action': '/booking/login/'})


@require_http_methods(['POST'])
@check_recaptcha
def InsertReservation(request):  # insert booking list
    try:
        # For validation
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
        if result == None or result == False:  # Using PC or No social login # Account Not Exist
            return redirect('/booking/login/',)
            # return redirect(reverse('member'),args=())
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error.html', {'error': result['error'], 'action': '/booking/login/'})
        # Account Exist
        # insert data
        user_id = request.POST.get('user_id', None)
        store_id = request.POST.get('store_id', None)
        bk_date = request.POST.get('bk_date', None)
        bk_st = request.POST.get('bk_st', None)
        bk_ed = request.POST.get('bk_ed', None)
        adult = request.POST.get('adult', None)
        children = request.POST.get('children', None)
        bk_ps = request.POST.get('bk_ps', None)
        event_type = request.POST.get('event_type', None)
        time_session = request.POST.get('time_session', None)
        entire_time = request.POST.get('entire_time', False)
        bk_price = request.POST.get('price', None)
        is_cancel = False
        waiting_num = 0
        # Check data format
        Bklist_Serializer(data={
            'user_id': user_id,
            'store_id': store_id,
            'bk_st': bk_st,
            'bk_ed': bk_ed,
            'adult': adult,
            'children': children,
            'bk_ps': bk_ps,
            'event_type': event_type,
            'time_session': time_session,
            'entire_time': entire_time,
            'bk_price': bk_price,
            'is_cancel': is_cancel,
            'is_cancel': is_cancel,
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
            if store_query.seat < total:
                raise Exception('超過總容納人數')
            # get the booking event of that time session
            bk_queryset = BkList.objects.select_for_update().filter(
                store_id=store_id,
                bk_date=bk_date,
                time_session=time_session,
                is_cancel=is_cancel,
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
            else: # don't need to wait
                waiting_num = 0

            final_queryset = BkList.objects.create(  # insert data
                user_id=user_id,
                store_id=store_id,
                bk_date=bk_date,
                bk_st=bk_st,
                bk_ed=bk_ed,
                adult=adult,
                children=children,
                bk_ps=bk_ps,
                event_type=event_type,
                time_session=time_session,
                entire_time=entire_time,
                is_cancel=is_cancel,
                waiting_num=waiting_num,
                bk_price=bk_price,
            )
            get_user_info = Account.objects.only('username').get(
                user_id=user_id,
                social_id=social_id,
                social_app=social_app,
            )

            get_store_name = Store.objects.only(
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
            store_serializer = Store_Serializer(get_store_name)
            bklist_serializer = Bklist_Serializer(final_queryset)

            request.session.flush()
            return render(request, 'reservation_finish.html', {
                'data': bklist_serializer.data,
                'store': store_serializer.data,
                'user_info': account_serializer.data, })
    except Exception as e:
        return render(request, 'error/error.html', {'error': e,'action':'/booking/login/'})


def login_portal(request):
    return render(request, 'login.html',)


def error(request):  # error page
    return render(request, 'error/error.html',{'action':'/booking/login/'})


@require_http_methods(['POST', 'GET'])
def member(request):
    try:  # Check Login
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.ClientAuthentication(
            social_id, social_app)  # queryset or something else
        if result == None:  # Using PC or No social login
            return redirect('/booking/login/',)
        elif result == False:  # Account Not Exist
            return render(request, 'member.html', {'google_keys': settings.RECAPTCHA_PUBLIC_KEY})
            # return redirect(reverse('member'),args=())
        # error occurred the type of result is {'error' : error}
        elif type(result) == dict:
            return render(request, 'error/error.html', {'error': result['error'],'action':'/booking/login/'})
        else:  # Account Exist
            serializer = Acc_Serializer(result)
            request.session['member_id'] = result.user_id

            return render(request, 'reservation.html', {
                'data': serializer.data,
                'google_keys': settings.RECAPTCHA_PUBLIC_KEY})

    except Exception as e:
        return render(request, 'error/error.html', {'error': e,'action':'/booking/login/'})


# Ajax api --------------------------------------------------------------
@require_http_methods(['POST'])
def getWaitingList(request):  # get waiting list
    try:
        bk_date = request.POST.get('event_date', None)
        store_id = request.POST.get('store_id', None)
        adult = request.POST.get('adult', None)
        children = request.POST.get('children', None)

        store_query = Store.objects.only('seat').get(
            store_id=store_id
        )

        bk_queryset = BkList.objects.filter(  # get all data
            store_id=store_id,
            bk_date=bk_date,
            is_cancel=False,
            # waiting_num__gt=0,
        )

        bk_list_noon = bk_queryset.filter(  # get bookinglist of noon
            waiting_num=0,
            time_session='Lunch'
        )
        bk_list_night = bk_queryset.filter(  # get bookinglist of night
            waiting_num=0,
            time_session='Dinner'
        )

        noon_count = 0  # Get number of noon total
        for i in bk_list_noon:
            if i.entire_time == True:
                noon_count = store_query.seat
            noon_count += int(i.children)+int(i.adult)

        noon_count += int(children)+int(adult)

        night_count = 0  # Get number of dinner total
        for i in bk_list_night:
            if i.entire_time == True:
                night_count = store_query.seat
            night_count += int(i.children)+int(i.adult)

        night_count += int(children)+int(adult)
    # judge if red or green
    # green = booking available, red = waiting line
        if noon_count > store_query.seat:
            status_noon = 'red'
        else:
            status_noon = 'green'

        if night_count > store_query.seat:
            status_night = 'red'
        else:
            status_night = 'green'

        lunch_waiting = bk_queryset.filter(  # Get waiting numbers lunch
            time_session='Lunch',
            waiting_num__gt=0,
        ).count()
        dinner_waiting = bk_queryset.filter(  # Get waiting numbers dinner
            time_session='Dinner',
            waiting_num__gt=0,
        ).count()

        if(lunch_waiting == 0 and status_noon == 'green'):
            lunch_waiting = '午餐: 可訂位'
        else:
            lunch_waiting = lunch_waiting + 1
            lunch_waiting = '午餐: 候補第 ' + str(lunch_waiting) + ' 順位'

        if (dinner_waiting == 0 and status_night == 'green'):
            dinner_waiting = '晚餐: 可訂位'
        else:
            dinner_waiting = dinner_waiting + 1
            dinner_waiting = '晚餐: 候補第 ' + str(dinner_waiting) + ' 順位'
        return JsonResponse({'lunch_status': lunch_waiting, 'dinner_status': dinner_waiting})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤','action':'/booking/login/'})


@require_http_methods(['POST'])
def getCalendar(request):  # full calendar
    try:
        store_id = request.POST.get('store_id', None)
        start_month = request.POST.get('start_month', None)
        end_month = request.POST.get('end_month', None)
        adult = request.POST.get('adult', None)
        children = request.POST.get('children', None)

        # Convert string to time
        start_month = datetime.strptime(start_month, '%Y-%m-%d').date()
        end_month = datetime.strptime(end_month, '%Y-%m-%d').date()

        # The days between start and end
        # days = (end_month-start_month).days()
        store_query = Store.objects.only('seat').get(
            store_id=store_id
        )
        # Get waiting list
        bk_queryset = BkList.objects.filter(  # get all available waiting_num
            store_id=store_id,
            bk_date__range=(start_month, end_month),
            is_cancel=False,
        )

        # get all orded reservation
        bookinglist = bk_queryset.filter(  # filter waiting_num != 0
            waiting_num=0,
        )
        # get all store events
        st_event = StoreEvent.objects.filter(  # StoreEvent
            store_id=store_id,
            event_date__range=(start_month, end_month),
        )

        event_arr = []
        for i in st_event:
            event_sub_arr = {}  # event dictionary
            if i.time_session == 'Lunch':
                i.time_session = '午餐'
            else:
                i.time_session = '晚餐'

            if i.event_type == 'rest':
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.event_date
                event_sub_arr['backgroundColor'] = 'yellow'
            elif i .event_type == 'rent':
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.event_date
                event_sub_arr['backgroundColor'] = 'yellow'
            event_arr.append(event_sub_arr)
        print('1: ', event_arr)
        for i in bookinglist:
            event_sub_arr = {}  # event dictionary
            # Convert time_session to chiness
            if i.time_session == 'Lunch':
                i.time_session = '午餐'
            else:
                i.time_session = '晚餐'

            if i.entire_time == True:
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.bk_date
                event_sub_arr['backgroundColor'] = 'red'
                # event_sub_arr['status'] = '候補'

            elif int(i.adult)+int(i.children)+int(adult)+int(children) > store_query.seat:
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.bk_date
                event_sub_arr['backgroundColor'] = 'red'

            else:
                event_sub_arr['title'] = i.time_session
                event_sub_arr['start'] = i.bk_date
                event_sub_arr['backgroundColor'] = 'green'

            event_arr.append(event_sub_arr)
        print('2: ', event_arr)
        return JsonResponse({'result': event_arr})
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤','action':'/booking/login/'})


# Test function ------------------------
def testtemplate(request):
    return render(request, 'reservation_finish.html')


class testView(APIView):  # render html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def post(self, request, format=None):
        try:
            self.template_name = 'booking.html'
            with transaction.atomic():  # transaction
                serializer = Acc_Serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': request.data}, status=status.HTTP_201_CREATED)
                else:
                    self.template_name = 'error/error.html'
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.template_name = 'error/error.html'
            return Response({'error': e})
