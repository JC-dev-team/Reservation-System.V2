from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'account',views.AccountViewSet) # The url will be booking/api/account
router.register(r'actionLog',views.ActionLogViewSet) # The url will be booking/api/actionLog
router.register(r'bookingList',views.BkListViewSet) # The url will be booking/api/bookingList
router.register(r'production',views.ProductionViewSet) # The url will be booking/api/production
router.register(r'store',views.StoreViewSet) # The url will be booking/api/store
router.register(r'staff',views.StaffViewSet) # The url will be booking/api/staff


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('member/', views.member, name='member'),
    path('error/', views.error, name='error'),
    path('api/', include(router.urls)), 
]
