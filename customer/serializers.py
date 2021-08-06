from rest_framework import serializers

from .models import *


class CustomerBriefListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'phone', 'first_name', 'last_name']
        read_only_fields = ['id']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = []
        read_only_fields = ['phone']


class AddressBriefListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['owner', 'title', 'state', 'city']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['owner']

