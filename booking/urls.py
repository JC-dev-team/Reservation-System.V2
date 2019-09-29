from django.urls import path
from . import views
from booking.views import hello_world

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',views.index,name='index'),
    path('', hello_world),
    

]