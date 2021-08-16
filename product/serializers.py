from rest_framework import serializers

from .models import Product, Category, Discount


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True, source='category.__str__')
    discount = serializers.PrimaryKeyRelatedField(source='discount.__str__', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'company_brand', 'category', 'discount',
                  'price', 'inventory', 'specifications']
        read_only_fields = ['id', 'discount']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_fa', 'ref_category']
        read_only_fields = ['id']


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        exclude = ['deleted']
