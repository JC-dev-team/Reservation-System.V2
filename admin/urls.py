from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    ## page 
    # /softwayliving/error/
    path('error/',views.error),
    # /softwayliving/login/
    path('login/', views.staff_login_portal,),
    # /softwayliving/StaffAuth/
    path('StaffAuth/',views.staff_auth,),
    # /softwayliving/checkreservation/
    path('checkreservation/',views.staff_check_reservation_page),
    # /softwayliving/reservation/
    path('reservation/',views.staff_reservation_page),
    


    ## Ajax api
    # /softwayliving/staff_check/
    path('staff_check/',views.staff_check_reservation),
    # /softwayliving/add_event/
    path('add_event/',views.staff_add_event),
    # /softwayliving/approval/
    path('approval/',views.staff_approval_reservation),
    # /softwayliving/delete/
    path('cancel/',views.staff_cancel_reservation),
]


