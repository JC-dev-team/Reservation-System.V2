from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    ## Page
    # /error/ 
    path('error/',views.error),
    # /preview/
    path('preview/',views.preview),
    # /
    path('',views.preview),
    # LineBot
    path('callback/',views.linebot_send_msg),
    
]

# handler404 = views.error_404_view

