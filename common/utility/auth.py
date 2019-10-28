from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect, reverse
from main.models import Account, Staff
from common.serializers import Acc_Serializer, Staff_Serializer
from django.db import transaction, DatabaseError
from functools import wraps
import os
import sys


class StaffAuthBackend(ModelBackend):
    def authenticate(self, request, email, password):
        try:
            if (email == None) or (password == None):  # Using PC or No social login
                return None
            else:   # parameter not None
                queryset = Staff.objects.get(
                    email=email,
                    password=password,
                )
                return queryset

        except Staff.DoesNotExist:  # Staff Not Exist
            return None
        # except Exception as e:
        #     return {'error': e}

    def get_user(self, staff_id):
        try:
            return Staff.objects.get(staff_id=staff_id)
        except Staff.DoesNotExist:
            return None


class ClientAuthBackend(ModelBackend):
    def authenticate(self, request, social_id=None, social_app=None):
        try:
            # Using PC or No social login
            if (social_id == None) or (social_app == None) or(social_id == '') or (social_app == ''):
                return None
            else:   # parameter not None
                with transaction.atomic():  # transaction
                    user = Account.objects.select_for_update().get(
                        social_id=social_id,
                        social_app=social_app,
                    )
                    return user
        except Account.DoesNotExist:  # Account Not Exist
            return False
        # except Exception as e:
        #     return {'error': e}

    def get_user(self, user_id):
        try:
            return Account.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

# decorators


def Client_login_required(function=None, redirect_url='/'):
    def wrapper(request):
        if request.session.get('user_id', None) == None or request.session.get('is_Login') != True:
            return redirect(redirect_url)
        else:
            return function(request)
    return wrapper


def ClientAuthentication(social_id, social_app):  # Account Check Auth
    try:
        # Using PC or No social login
        if (social_id == None) or (social_app == None) or(social_id == '') or (social_app == ''):
            return None
        else:   # parameter not None
            with transaction.atomic():  # transaction
                User = Account.objects.select_for_update().get(
                    social_id=social_id,
                    social_app=social_app,
                )
                # serializer = Acc_Serializer(queryset)
                return User
    except Account.DoesNotExist:  # Account Not Exist
        return False
    except Exception as e:
        return {'error': e}


def StaffAuthentication(email, password):  # staff account checking
    try:
        if (email == None) or (password == None):  # Using PC or No social login
            return None
        else:   # parameter not None
            queryset = Staff.objects.get(
                email=email,
                password=password,
            )
            serializer = Staff_Serializer(queryset)
            return serializer.data

    except Staff.DoesNotExist:  # Account Not Exist
        return False
    except Exception as e:
        return {'error': e}
