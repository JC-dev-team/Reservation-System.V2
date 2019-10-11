from datetime import datetime
from django.shortcuts import render, redirect, reverse
# from .models import ActionLog, BkList, Account, Production, Staff, Store
# from .serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from . import auth
from django.db import transaction, DatabaseError
from django.db.models import Q  # complex lookup

def error(request):
    return render(request, 'error/error.html')

# admin dashboard -------------------


def staff_login(request):  # authentication staff
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        result = auth.StaffAuthentication(social_id, social_app)

        if result == None or result == False:
            return render(request, 'error/error404.html')

        elif list(result.keys())[0] == 'error':  # error occurred
            return render(request, 'error/error.html', {'error': result['error']})
        else:
            return render(request, 'admin_dashboard.html', {'data': result})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def staff_checkbooking(request):
    try:
        store_id = request.POST.get('store_id', None)
        bk_date = request.POST.get('bk_date', None)

        pass
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def staff_approval_booking(request):
    try:
        bk_id = request.POST.get('bk_id', None)
        pass
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})