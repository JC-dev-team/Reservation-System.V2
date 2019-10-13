from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf.urls import handler404
# ## Maybe need to remove in future
# router = DefaultRouter()
# # The url will be booking/api/account
# router.register(r'account', views.AccountViewSet)

# # The url will be booking/api/actionLog
# router.register(r'actionLog', views.ActionLogViewSet)

# # The url will be booking/api/bookingList
# router.register(r'bookingList', views.BkListViewSet)

# # The url will be booking/api/production
# router.register(r'production', views.ProductionViewSet)

# # The url will be booking/api/store
# router.register(r'store', views.StoreViewSet)

# # The url will be booking/api/staff
# router.register(r'staff', views.StaffViewSet)



urlpatterns = [
    path('login/', views.login_portal, name='login'),
    path('member/', views.member, name='member'),
    path('reservation/', views.InsertReservation, name='InsertReservation'),
    path('booking/',views.ToBookingView),
    path('getCalendar/',views.getCalendar, name='getCalendar'),
    path('error/',views.error, name='error'),
    path('getWaitingList/',views.getWaitingList, name='getWaitingList'),

    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    
    # Test Views deploy delete 
    path('test001/',views.testView),
    path('testtemplate/',views.testtemplate, name='testtemplate'),
    
]

# handler404 = views.error_404_view

