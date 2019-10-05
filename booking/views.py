from django.shortcuts import render, redirect, reverse
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
from . import common as com

# class isLogin(BasePermission):
#     message = 'no perosn login'
#     def has_permission(self, request, view):
#         member = request.query_params.get("apikey",0)
#         return super().has_permission(request, view)


class AccountViewSet(viewsets.ModelViewSet):  # api get account data
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer

    def get_queryset(self):
        queryset = self.queryset
        phone = self.request.query_params.get('phone', None)
        social_id = self.request.query_params.get('social_id', None)

        query_set = queryset.filter(phone=phone)
        return query_set


def test(request):  # render html
    phone = request.POST.get('phone', None)
    username = request.POST.get('username', None)
    social_id = request.POST.get('social_id', None)
    social_app = request.POST.get('social_app', None)

    queryset = Account.objects.create(
        phone=phone,
        username=username,
        social_id=social_id,
        social_app=social_app
    )
    queryset = Account.objects.get(
        phone=phone,
        username=username,
        social_id=social_id,
        social_app=social_app
    )
    serializer_class = Acc_Serializer(queryset)
    return render(request, 'booking.html', {'data': serializer_class.data})


class ToBookingView(APIView):  # render html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def post(self, request, format=None):
        try:
            self.template_name = 'booking.html'
            serializer = Acc_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': request.data}, status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'exception': e})

    def get(self, request, format=None):
        try:
            social_id = request.query_params.get('social_id', None)
            social_app = request.query_params.get('social_app', None)

            queryset = Account.objects.filter(
                social_id=social_id,
                social_app=social_app,
            )
            if len(queryset) == 0:
                self.template_name = 'member.html'
                return
            elif len(queryset) == 1:
                self.template_name = 'booking.html'
                serializer_class = Acc_Serializer(queryset)
                return Response({'data': serializer_class.data}, status=status.HTTP_201_CREATED)
            else:
                return
        except:
            return Http404("Data not found")


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


def login(request):
    return render(request, 'login.html',)


def reservation(request):
    return render(request, 'reservation.html')


def member(request):
    social_id = request.POST.get('social_id', None)
    social_app = request.POST.get('social_app', None)
    print(social_id,social_app)
    result = com.CheckClientAuth(social_id, social_app)
    print(social_id, social_app)
    if result == None:  # Using PC or No social login
        return reverse('login.html',)
    elif result == False:  # Account Not Exist
        return render(request, 'member.html',)
    elif list(result.keys())[0] == 'error':  # error occurred
        return render(request, '/error/error.html', {'error': result.error})
    else:  # Account Exist
        return render(request, 'reservation.html', {'data': result})


def checkbooking(request):
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        queryset = BkList.objects.get(
            social_id=social_id,
            social_app=social_app,
        )

        serializer = Acc_Serializer(queryset)
        return render(request, 'checkbooking.html', {'data': serializer.data})
    except Exception as e:
        return render(request, '/error/error.html', {'error': e})


def testtemplate(request):
    return render(request, 'test.html')
