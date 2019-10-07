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
from django.db import transaction, DatabaseError

# ----- Class site ----------------------


class AccountViewSet(viewsets.ModelViewSet):  # api get account data
    queryset = Account.objects.all()
    serializer_class = Acc_Serializer

    def get_queryset(self):
        queryset = self.queryset
        phone = self.request.query_params.get('phone', None)
        social_id = self.request.query_params.get('social_id', None)

        query_set = queryset.filter(phone=phone)
        return query_set


class ToBookingView(APIView):  # render html
    renderer_classes = [TemplateHTMLRenderer]
    template_name = None

    def post(self, request, format=None):
        try:
            self.template_name = 'reservation.html'
            with transaction.atomic():  # transaction
                serializer = Acc_Serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': request.data}, status=status.HTTP_201_CREATED)
                else:
                    self.template_name = 'error/error.html'
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.template_name = 'error/error.html'
            return Response({'error': e})


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

# Definition site ------------------------------------------------


def booking_list(request):
    try:
        # phone = request.POST.get('phone', None)

        return render(request, '')
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


def login(request):
    return render(request, 'login.html',)


def reservation(request):
    return render(request, 'reservation.html')


def member(request):
    social_id = request.POST.get('social_id', None)
    social_app = request.POST.get('social_app', None)
    result = com.Authentication(social_id, social_app)
    if result == None:  # Using PC or No social login
        return redirect('/booking/login/',)
    elif result == False:  # Account Not Exist
        return render(request, 'member.html',)
        # return redirect(reverse('member'),args=())
    elif list(result.keys())[0] == 'error':  # error occurred
        print('result: ', result)
        return render(request, 'error/error.html', {'error': result['error']})
    else:  # Account Exist
        return render(request, 'reservation.html', {'data': result})


def checkbooking(request):
    try:
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        queryset = BkList.objects.select_for_update().get(  # sql for update
            social_id=social_id,
            social_app=social_app,
        )
        serializer = Acc_Serializer(queryset)
        return render(request, 'checkbooking.html', {'data': serializer.data})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})


# Test function ------------------------
def testtemplate(request):
    return render(request, 'test/test.html')


def test(request):  # render html
    try:
        phone = request.POST.get('phone', None)
        username = request.POST.get('username', None)
        social_id = request.POST.get('social_id', None)
        social_app = request.POST.get('social_app', None)
        with transaction.atomic():  # transaction
            queryset = Account.objects.create(
                phone=phone,
                username=username,
                social_id=social_id,
                social_app=social_app,
            )
        queryset = Account.objects.get(
            phone=phone,
            username=username,
            social_id=social_id,
            social_app=social_app
        )

        # serializer_class = Acc_Serializer
        return render(request, 'test/booking.html', {'data': queryset})
    except Exception as e:
        return render(request, 'error/error.html', {'error': e})
