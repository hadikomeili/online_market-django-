from rest_framework import serializers

from product.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'company_brand', 'category', 'discount',
                  'price', 'inventory', 'specifications']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_fa']
        read_only_fields = ['id']