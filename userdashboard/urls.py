from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('error/',views.error,),
    path('user_check_reservation/',views.user_check_reservation, name='user_check_reservation'),
    path('user_remove_reservation/',views.user_remove_reservation, name='user_remove_reservation'),
    path('user_login/',views.user_login, name='user_login'),
    path('user_auth',views.user_auth, name='user_auth'),
    
]


