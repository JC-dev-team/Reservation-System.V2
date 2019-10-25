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
    # /softwayliving/admin_reservation/
    path('admin_reservation/',views.staff_add_reservation),
    # /softwayliving/member_list/
    path('member_list/',views.member_management),
    
    ## Ajax api
    # /softwayliving/staff_check/
    path('staff_check/',views.staff_check_reservation),
    # /softwayliving/add_event/
    path('add_event/',views.staff_add_event),
    # /softwayliving/confirm/
    path('confirm/',views.staff_confirm_reservation),
    # /softwayliving/delete/
    path('cancel/',views.staff_cancel_reservation),
    # /softwayliving/pass/ 
    path('pass/',views.staff_pass_reservation),
    # /softwayliving/waiting/
    path('waiting/',views.staff_is_waiting), # 候補
    # /softwayliving/confirm/
    path('is_confirm/',views.staff_is_confirmed), # 已確認
    # /softwayliving/not_confirmed/
    path('not_confirm/',views.staff_not_confirmed), # 待確認
    # /softwayliving/canceled/
    path('delete/',views.staff_is_cancel), # 已刪除
    # /softwayliving/remove_member/
    path('remove_member/',views.staff_remove_member),


]


