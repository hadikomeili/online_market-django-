from rest_framework import serializers

from customer.models import Customer
from product.models import Product
from .models import OrderItem, Cart


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(queryset=Product.objects.all(),
                                                  view_name='product:product_details')
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id']


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.HyperlinkedRelatedField(queryset=Customer.objects.all(),
                                                   view_name='customer:customer_card')

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id']