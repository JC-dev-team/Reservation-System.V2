from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'account',views.AccountViewSet) # The url will be /api/account

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.booking_index, name='bk_index'),
    path('api/', include(router.urls)), 
]
