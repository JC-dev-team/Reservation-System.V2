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
    path('checkreservation/',views.staff_check_reservation_page,),
    # /softwayliving/reservation/
    path('reservation/',views.staff_reservation_page),
    # /softwayliving/admin_reservation/
    path('admin_reservation/',views.staff_add_reservation),
    # /softwayliving/member_list/
    path('member_list/',views.member_management),
    # /softwayliving/insert_bk/
    path('insert_bk/',views.admin_InsertReservation),
    # /softwayliving/productions/
    path('productions/',views.staff_productions_page),
    # /softwayliving/admins/
    path('admins/',views.staff_admins_page),
    # /softwayliving/stores/
    path('stores/',views.staff_stores_page),
    # /softwayliving/logout/
    path('logout/',views.staff_logout),


    ## Ajax api

    ### Event API
    # /softwayliving/add_event/
    path('add_event/',views.staff_add_event),
    # /softwayliving/cancel_event/
    path('cancel_event/',views.staff_cancel_event),

    ### Reservation API
    # /softwayliving/staff_check/
    path('staff_check/',views.staff_check_reservation),
    # /softwayliving/confirm/
    path('confirm/',views.staff_confirm_reservation),
    # /softwayliving/delete/
    path('cancel/',views.staff_cancel_reservation),
    # /softwayliving/pass/ 
    path('pass/',views.staff_pass_reservation),

    ### reservation's category
    # /softwayliving/waiting/
    path('waiting/',views.staff_is_waiting), # get候補
    # /softwayliving/confirm/
    path('is_confirm/',views.staff_is_confirmed), # get已確認
    # /softwayliving/not_confirmed/
    path('not_confirm/',views.staff_not_confirmed), # get待確認
    # /softwayliving/canceled/
    path('delete/',views.staff_is_cancel), # get已刪除

    ### member Info operations
    # /softwayliving/lock_member/
    path('lock_member/',views.staff_lock_member),
    # /softwayliving/lock_member/
    path('unlock_member/',views.staff_unlock_member),
    # /softwayliving/modify_member/
    path('modify_member/',views.staff_modify_member),

    ### Productions api
    # /softwayliving/AddProduct/
    path('AddProduct/',views.add_product),
    # /softwayliving/ModifyProduct/
    path('ModifyProduct/',views.modify_product),
    # /softwayliving/DeleteProduct/
    path('DeleteProduct/',views.delete_product),

    ### admin api
    # /softwayliving/AddAdmin/
    path('AddAdmin/',views.add_admin),
    # /softwayliving/ModifyAdmin/
    path('ModifyAdmin/',views.modify_admin),
    # /softwayliving/DeleteAdmin/
    path('DeleteAdmin/',views.delete_admin),
    # /softwayliving/ModifyPwd/
    path('ModifyPwd/',views.modify_pwd),

    ### Store api
    # /softwayliving/AddStore/
    path('AddStore/',views.add_store),
    # /softwayliving/ModifyStore/
    path('ModifyStore/',views.modify_store),
    # /softwayliving/DeleteStore/
    path('DeleteStore/',views.delete_store),


    ## Test
    # path('eve/',views.event_AAAA),

]


