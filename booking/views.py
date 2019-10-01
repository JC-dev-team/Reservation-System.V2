from django.shortcuts import render, redirect
from . import models
from .serializers import account
from rest_framework import viewsets

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
