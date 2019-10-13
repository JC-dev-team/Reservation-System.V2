from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_portal,),
    path('auth/',views.dashboard,),


    
]


