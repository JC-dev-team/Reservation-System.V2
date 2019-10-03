from django.shortcuts import render, redirect
from .models import ActionLog, BkList, Account, Production, Staff, Store
from .serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

# Create your views here.
# class isLogin(BasePermission):
#     message = 'no perosn login'
#     def has_permission(self, request, view):
#         member = request.query_params.get("apikey",0)
#         return super().has_permission(request, view)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer
    def get_queryset(self):
        # queryset = Account.objects.all()
        queryset = self.queryset
        phone=self.request.query_params.get('phone',None)
        query_set = queryset.filter(phone=phone)
        return query_set

def test(request):
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer(queryset, many=True)

    return render(request, 'booking.html', {'data': serializer_class.data})


class testView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'booking.html'

    def get(self, request,pk):
        queryset = Account.objects.all()
        serializer_class = Acc_Serializer(queryset, many=True)
        return Response({'data': pk})


class ActionLogViewSet(viewsets.ModelViewSet):
    queryset = ActionLog.objects.all()
    serializer_class = Actlog_Serializer


class BkListViewSet(viewsets.ModelViewSet):
    queryset = BkList.objects.all()
    serializer_class = Bklist_Serializer


class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = Prod_Serializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = Store_Serializer
    permission_classes = (IsAuthenticated,)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = Staff_Serializer


def member(request):
    for i in request:
        print(len(request))
    return render(request, 'member.html',)
