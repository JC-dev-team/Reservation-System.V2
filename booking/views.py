from django.shortcuts import render, redirect
from . import models
from .serializers import account, action_log, bk_list, production, staff, store
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer


# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = account.objects.all()
    serializer_class = account



# def booking_index(request):
#     return render(request,'book_index.html',)

# def insert_accounts(request):
#     try:
#         models.objects.get
#         models.objects.create(user_id='',)
#         return 
#     except :

#         return 
    
# def query_member(request):
#     return render
#
#
# def insert_member(request):
#     return redirect
