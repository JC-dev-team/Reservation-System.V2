from rest_framework import serializers
from main.models import Account, BkList, Production, Staff, Store, StoreEvent


class check_bklist(serializers.ModelSerializer):
    class Meta:
        model = BkList
        fields = ('user_id', 'store_id', 'bk_date', 'bk_st',
                  'bk_ed', 'adult', 'children', 'bk_ps', 'bk_habit','event_type', 
                  'time_session', 'entire_time', 'bk_price','is_confirm')

class checkAuth(serializers.ModelSerializer):
    class Meta:
        model =Account
        fields =('social_id','social_app')

class checkStaffAuth(serializers.ModelSerializer):
    class Meta:
        model =Staff
        fields =('social_id','social_app')

class applymember(serializers.ModelSerializer):
    class Meta:
        model =Account
        fields =('social_id','social_app','social_name','phone','username')


class Acc_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        # fields = ('user_id', 'social_id', 'social_app', 'username', 'phone','birth',)

class Bklist_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BkList
        fields = '__all__'


class Prod_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'


class Staff_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class Store_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class Store_form_serializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id', 'store_name','store_address','store_phone')



class StoreEvent_Serializer(serializers.ModelSerializer):
    class Meta:
        model = StoreEvent
        fields = '__all__'