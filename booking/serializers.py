from rest_framework import serializers
from .models import Account


class account(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        # fields =()