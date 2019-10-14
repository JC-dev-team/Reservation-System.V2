from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('error/',views.error,),
    path('checkreservation/',views.user_check_reservation, name='user_check_reservation'),
    path('removereservation/',views.user_remove_reservation, name='user_remove_reservation'),
    path('login/',views.user_login, name='user_login'),
    path('auth/',views.user_auth, name='user_auth'),
    # path()
]


