from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


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
    path('member/', views.member, name='member'),
    path('testtemplate/', views.testtemplate, name='testtemplate'),
    path('api/', include(router.urls)),
    path('test001/',views.test),
    path('test01/',views.testView.as_view()),
    # path('test/',views.check_members)
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('error/', views.error, name='error'),
]


