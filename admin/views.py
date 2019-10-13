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
from django.views.decorators.http import require_http_methods


def error(request):
    return render(request, 'error/error.html')

# admin dashboard -------------------


@require_http_methods(['POST', 'GET'])
def staff_login(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)

        print(social_id)
        print(social_app)
        # Check data format
        valid = checkAuth(data={
            'social_id': social_id,
            'social_app': social_app
        })
        if valid.is_valid() == False:
            raise Exception('Not valid, 帳號資料錯誤')

        result = auth.StaffAuthentication(social_id, social_app)
        
        if result == None or result == False:
            return render(request, 'error/error404.html')

        elif list(result.keys())[0] == 'error':  # error occurred
            return render(request, 'error/error.html', {'error': result['error']})
        else:
            return render(request, 'admin_dashboard.html', {'data': result})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


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
        )
        serializers = Bklist_Serializer(bk_queryset, many=True)

        return JsonResponse({'result': serializers.data})

    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])
def staff_approval_reservation(request):
    try:
        bk_uuid = request.POST.get('bk_uuid', None)
        with transaction.atomic():  # transaction
            bk_queryset = BkList.objects.select_for_update().get(
                bk_uuid=bk_uuid,
                is_cancel=False,

            )
            bk_queryset.update(waiting_num=0)  
            return JsonResponse({'result': True})
        
    except BkList.DoesNotExist:
        return JsonResponse({'error': '資料不存在'})            
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])
def staff_add_reservation(request):  # Help client to add reservation
    try:
        
        pass
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})


@require_http_methods(['POST'])
def staff_add_rest(request):
    try:
        pass
    except Exception as e:
        return JsonResponse({'error': '發生未知錯誤'})
