from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    # /userdashboard/error/
    path('error/', views.error,),

    # /userdashboard/checkreservation/
    path('checkreservation/', views.user_check_reservation,
         name='user_check_reservation'),

    # /userdashboard/login/
    path('login/', views.user_login, name='user_login'),

    # /userdashboard/auth/
    path('auth/', views.user_auth, name='user_auth'),

    # Ajax API
    # /userdashboard/removereservation/
    path('removereservation/', views.user_remove_reservation,
         name='user_remove_reservation'),
]
