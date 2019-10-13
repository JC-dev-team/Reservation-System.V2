from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_portal,),
    path('StaffAuth/',views.staff_auth,),
    path('checkreservation/',views.check_reservation),
    path('reservation/',views.reservation),
    # Ajax api
    path('staff_check/',views.staff_check_reservation),
    path('add_rest/',views.staff_add_rest),
    path('approval/',views.staff_approval_reservation),

]


