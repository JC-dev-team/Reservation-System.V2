# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend
# from django.shortcuts import render, redirect, reverse
# from .models import Account, Staff
# from .serializers import Acc_Serializer
# from django.db import transaction, DatabaseError
# from functools import wraps
# sys.path.append(os.path.join(settings.BASE_DIR, 'utility'))

# def Clientlogin_required(fun):
#     def wrapper(request):
#         social_id = request.POST.get('social_id', None)
#         social_app = request.POST.get('social_app', None)
#         result = ClientAuthentication()
#         if result == None:  # Using PC or No social login
#             return redirect('/booking/login/',)
#         elif result == False:  # Account Not Exist
#             return render(request, 'member.html',)
#         elif list(result.keys())[0] == 'error':  # error occurred
#             return render(request, 'error/error.html', {'error': result['error']})
#         else:  # Account Exist
#             # request.session['member_id'] = result.user_id
#             return wrapper


# def ClientAuthentication(social_id, social_app):  # Account Check Auth
#     try:
#         if (social_id == None) or (social_app == None):  # Using PC or No social login
#             return None
#         else:   # parameter not None
#             with transaction.atomic():  # transaction
#                 User = Account.objects.select_for_update().get(
#                     social_id=social_id,
#                     social_app=social_app,
#                 )
#                 # serializer = Acc_Serializer(queryset)
#                 return User
#     except Account.DoesNotExist:  # Account Not Exist
#         return False
#     except Exception as e:
#         return {'error': e}
