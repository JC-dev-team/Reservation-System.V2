from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

urlpatterns = [
    path('error/',views.error),
    path('login/', views.staff_login_portal,),
    path('StaffAuth/',views.staff_auth,),
    path('checkreservation/',views.staff_check_reservation_page),
    path('reservation/',views.staff_reservation_page),
    # Ajax api
    path('staff_check/',views.staff_check_reservation),
    path('add_rest/',views.staff_add_rest),
    path('approval/',views.staff_approval_reservation),

]


