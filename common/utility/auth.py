from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect, reverse
from main.models import Account, Staff
from common.serializers import Acc_Serializer, Staff_Serializer
from django.db import transaction, DatabaseError
from functools import wraps
import os
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
import uuid

User = get_user_model()

class StaffAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            flag=request.POST.get('flag',None)
            if (email == None) or (password == None):  # Using lost require values
                return None
            else:   # parameter not None
                User_data = User.objects.get(
                    email=email,
                )
                if flag == None:
                    result = check_password(password, User_data.password)
                    if result == False:
                        return None
                elif flag != None:
                    with transaction.atomic():  # transaction
                        password = make_password(password)
                        User_data.password = password
                        User_data.save()
                return User_data
        except User.DoesNotExist:  # Staff Not Exist
            return None

    def get_user(self, staff_id):
        try:
            return User.objects.get(pk=staff_id)
        except User.DoesNotExist:
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

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# decorators


def valid_pass_test(test_fun, redirect_url='/'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_fun(request.session):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        return _wrapped_view
    return decorator

# Client Login
def _login_required(function=None, redirect_url='/'):
    actual_decorator = valid_pass_test(
        lambda u: u.get('is_Login', False),
        redirect_url=redirect_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def ClientAuthentication(social_id, social_app):  # Account Check Auth
    try:
        # Using PC or No social login
        if (social_id == None) or (social_app == None) or(social_id == '') or (social_app == ''):
            return None
        else:   # parameter not None
            User = Account.objects.get(
                social_id=social_id,
                social_app=social_app,
            )
            return User
    except Account.DoesNotExist:  # Account Not Exist
        return False
    except Exception as e:
        return {'error': e}


def StaffAuthentication(email, password):  # staff account checking
    try:
        if (email == None) or (password == None):  # Not
            return None
        else:   # parameter not None
            queryset = Staff.objects.get(
                email=email,
            )
            if check_password(password,queryset.password):
                serializers = Staff_Serializer(queryset)
                return serializers.data
            else:
                return 'ERROR'
            
    except Staff.DoesNotExist:  # Account Not Exist
        return False
    except Exception as e:
        return {'error': e}


def create_passwords(string_length=8):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.
