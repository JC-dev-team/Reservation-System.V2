from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import Account
from .serializers import Acc_Serializer

# class LoginBackend(ModelBackend):

def CheckClientAuth(social_id, social_app): # Account Check Auth
    try:
        if (social_id == None) or (social_app == None): # Using PC or No social login
            return None
        else :   # Account Exist
            queryset = Account.objects.get(
                social_id=social_id,
                social_app=social_app,
            )
            serializer = Acc_Serializer(queryset)
            return  serializer.data
    except Account.DoesNotExist: # Account Not Exist
        return False
    except Exception as e:
        return {'error':e}
    
