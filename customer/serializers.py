from rest_framework import serializers

from .models import *


class CustomerBriefListSerializer(serializers.ModelSerializer):
    """
    for superuser use
    """

    class Meta:
        model = Customer
        fields = ['id', 'phone', 'first_name', 'last_name']
        read_only_fields = ['id', 'phone']


class CustomerDetailAdminSerializer(serializers.ModelSerializer):
    """
    for superuser use
    """
    id = serializers.HyperlinkedRelatedField(view_name='customer:customer_detail_api_for_admin', read_only=True)

    class Meta:
        model = Customer
        exclude = ['password']
        read_only_fields = ['id', 'phone', 'username', 'last_login']


class CustomerSerializer(serializers.ModelSerializer):
    """
    for customer use
    """
    class Meta:
        model = Customer
        fields = ['id', 'username', 'phone', 'first_name', 'last_name', 'national_code', 'gender', 'birthday', 'image']
        read_only_fields = ['id', 'phone', 'username']


class AddressBriefListSerializer(serializers.ModelSerializer):
    """
    for superuser use
    """
    owner = CustomerDetailAdminSerializer(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'title', 'state', 'city', 'rest_of_address', 'post_code', 'owner']
        read_only_fields = ['owner']


class AddressDetailSerializer(serializers.ModelSerializer):
    """
    for customer use
    """
    id = serializers.HyperlinkedRelatedField(view_name='customer:customer_address_detail_api', read_only=True)

    class Meta:
        model = Address
        exclude = ['deleted', 'create_timestamp', 'modify_timestamp', 'delete_timestamp', 'owner']
        read_only_fields = ['id', ]


