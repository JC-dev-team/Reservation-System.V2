from datetime import datetime
from django.shortcuts import render, redirect, reverse
from booking.models import ActionLog, BkList, Account, Production, Staff, Store
from common.serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
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

def check_reservation(request):
    try:
        store_id = request.POST.get('store_id', None)
        # bk_date = request.POST.get('bk_date',None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)

        

        acc_queryset = Account.objects.only('user_id').get(
            social_id=social_id,
            social_app=social_app,
        )
        queryset = BkList.objects.filter(
            user_id=acc_queryset.user_id,
            store_id=store_id,
        )

        serializer = Acc_Serializer(queryset)
        return render(request, 'check_reservation.html', {'data': serializer.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})

