from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('error/',views.error,name='error_check'),
    path('check_reservation/',views.check_reservation, name='check_reservation'),
    path('remove_reservation/',views.remove_reservation, name='remove_reservation'),
    path('user_login/',views.user_login, name='user_login'),
    
]


