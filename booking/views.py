from django.shortcuts import render, redirect
from .models import ActionLog, BkList, Account, Production, Staff, Store
from .serializers import Acc_Serializer, Actlog_Serializer, Bklist_Serializer, Prod_Serializer, Staff_Serializer, Store_Serializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404

# Create your views here.
# class isLogin(BasePermission):
#     message = 'no perosn login'
#     def has_permission(self, request, view):
#         member = request.query_params.get("apikey",0)
#         return super().has_permission(request, view)


class AccountViewSet(viewsets.ModelViewSet):  # api get account data
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer

    def get_queryset(self):
        # queryset = Account.objects.all()
        queryset = self.queryset
        phone = self.request.query_params.get('phone', None)
        social_id = self.request.query_params.get('social_id', None)
        query_set = queryset.filter(phone=phone)
        return query_set
    

def test(request):  # render html
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer(queryset, many=True)

    return render(request, 'booking.html', {'data': serializer_class.data})


class testView(APIView):  # render html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'booking.html'

    def post(self, request, format=None):
        serializer = Acc_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':request.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        phone = request.query_params.get('phone', None)
        queryset = Account.objects.filter(phone=phone)
        serializer_class = Acc_Serializer(queryset, many=True)
        return Response({'data': serializer_class.data},status=status.HTTP_201_CREATED)

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

    return render(request, 'member.html',)


def testtemplate(request):
    return render(request, 'test.html')
