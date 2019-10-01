from rest_framework import serializers
from .models import Account,ActionLog, BkList, Production, Staff, Store


class account(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        # fields =()

class action_log(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'

class bk_list(serializers.ModelSerializer):
    class Meta:
        model = BkList
        fields = '__all__'

class production(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'


class staff(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class store(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

