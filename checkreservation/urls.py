from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('error/',views.error, name='error'),
    # path('check_reservation/',views.check_reservation, name='check_reservation'),
    
]


