from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

## Maybe need to remove in future
router = DefaultRouter()
# The url will be booking/api/account
router.register(r'account', views.AccountViewSet)

# The url will be booking/api/actionLog
router.register(r'actionLog', views.ActionLogViewSet)

# The url will be booking/api/bookingList
router.register(r'bookingList', views.BkListViewSet)

# The url will be booking/api/production
router.register(r'production', views.ProductionViewSet)

# The url will be booking/api/store
router.register(r'store', views.StoreViewSet)

# The url will be booking/api/staff
router.register(r'staff', views.StaffViewSet)



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.login_portal, name='login'),
    path('member/', views.member, name='member'),
    path('reservation/', views.reservation, name='reservation'),
    # path('api/', include(router.urls)),
    path('booking/',views.ToBookingView),
    path('getCalendar/',views.getCalendar, name='getCalendar'),
    path('error/',views.error, name='error'),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #checking system
    path('check_reservation/',views.check_reservation, name='check_reservation'),
    
    
    # Test Views deploy delete 
    path('test001/',views.testView),
    path('testtemplate/',views.testtemplate, name='testtemplate'),
    path('test_check_reservation/',views.test_check_reservation, name='test_check_reservation'),
    
]


