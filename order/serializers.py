from rest_framework import serializers
from customer.models import Customer, Address
from product.models import Product
from product.serializers import ProductSerializer
from .models import OrderItem, Cart


class OrderItemSerializer(serializers.ModelSerializer):
    """
    for superuser
    """
    product = serializers.HyperlinkedRelatedField(queryset=Product.objects.all(),
                                                  view_name='product:product_details_api')
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id']


class OrderItemForCustomerSerializer(serializers.ModelSerializer):
    """
    for customer
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cart = serializers.PrimaryKeyRelatedField(read_only=True, source='cart.customer.__str__')

    class Meta:
        model = OrderItem
        fields = ['id', 'cart', 'product', 'product_number', 'calculate_order_item_price']
        read_only_fields = ['id', 'calculate_order_item_price', 'cart', 'product']


class CartSerializer(serializers.ModelSerializer):
    """
    for superuser
    """
    customer = serializers.HyperlinkedRelatedField(queryset=Customer.objects.all(),
                                                   view_name='customer:customer_detail_api_for_admin')

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id']


class CartForCustomerSerializer(serializers.ModelSerializer):
    """
    for customer
    """
    customer = serializers.PrimaryKeyRelatedField(read_only=True, source='customer.__str__')
    order_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'order_status', 'final_price', 'order_address']
        read_only_fields = ['id', 'customer', 'order_status', 'final_price']


