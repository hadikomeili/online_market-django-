from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer
from .models import *
from rest_framework import generics
from customer.permissions import *


# Create your views here.

###---Product---###


class ProductIndexView(generic.TemplateView):
    """
    View class for display all products
    """

    ### task: logging ###

    import logging
    logger = logging.getLogger('project.developers')
    logger.debug("Debug msg!")
    logger.info("Info msg!")
    logger.warning("Warning msg!")
    logger.error("Error msg!")
    logger.critical("Critical msg!")

    template_name = 'product/index.html'
    extra_context = {
        'products': Product.objects.all(),
        'category': Category.objects.all().filter(ref_category=None),
    }


class ProductDetailsView(generic.DetailView):
    """
    View class for display a product details
    """
    template_name = 'product/detail.html'
    model = Product
    context_object_name = 'product_details'


class ProductCardView(generic.DetailView):
    """
    View class for create card view for a product
    """
    template_name = 'product/card.html'
    model = Product
    context_object_name = 'product_card'


# class CategoryIndexView(generic.TemplateView):
#     """
#     View class for display all categories
#     """
#     template_name = 'product/category_index.html'
#     extra_context = {
#         'category': Category.objects.all()
#     }


class CategoryView(View):
    """
    View class for display products based on its category
    """

    def get(self, request, *args, **kwargs):
        category_id = kwargs['id']
        cat = Category.objects.get(id=category_id)
        cats = []
        for c in Category.objects.all():
            if c.ref_category == cat:
                cats.append(c)

        products = []
        for product in Product.objects.all():
            for x in cats:
                if product.category == x:
                    products.append(product)

        category = Category.objects.all().filter(ref_category=None)
        return render(request, 'product/category_index.html', {'products': products, 'category': category})


class CategoryCardView(generic.DetailView):
    """
    View class for create card view for a category
    """
    template_name = 'product/category_panel.html'
    model = Category
    context_object_name = 'category'


# -----------------------API_Views-----------------------#


# @api_view(['GET', 'POST'])
# def product_list_view_api(request):
#     """
#     a function view for product list as api
#     """
#     if request.method == 'GET':
#         products = Product.objects.all()
#         s = ProductSerializer(products, many=True)
#         return Response({'products': s.data})
#     elif request.method == 'POST':
#         print(request.data)
#         new_product = ProductSerializer(data=request.data)
#         print(new_product)
#         if new_product.is_valid():
#             new_product.save()
#             return Response(new_product.data)
#         else:
#             return Response(new_product.errors)


# @csrf_exempt
# @api_view(['GET', 'POST'])
# def category_list_view_api(request):
#     """
#     a function view for category list as api
#     """
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         s = CategorySerializer(categories, many=True)
#         return Response({'categories': s.data})
#     elif request.method == 'POST':
#         new_cat = CategorySerializer(data=request.POST)
#
#         if new_cat.is_valid():
#
#             return Response(new_cat.data)
#         else:
#             return Response(new_cat.errors, status=400)


class ProductAPIView(generics.ListCreateAPIView):
    """
    API view for superuser to see products list and create new product
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class ProductDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for superuser to see product details and modify or delete product
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class ProductsIndexAPIView(generics.ListAPIView):
    """
    API view for customer to see products list
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailsIndexAPIView(generics.RetrieveAPIView):
    """
    API view for customer to see product details
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryListAPIView(generics.ListCreateAPIView):
    """
    API view for superuser to see categories list and create new category
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for superuser to see category details and modify or delete category
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CategoryIndexAPIView(generics.ListAPIView):
    """
    API view for customer to see categories list
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailsIndexAPIView(generics.RetrieveAPIView):
    """
    API view for customer to see category details
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class DiscountAPIView(generics.ListCreateAPIView):
    """
    API view for superuser to see discounts list and create new discount model
    """
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for superuser to see discount details and modify or delete discount model
    """
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]