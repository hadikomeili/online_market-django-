from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import Http404, HttpResponse

from .models import *


# Create your views here.

###---Product---###

class ProductIndexView(generic.TemplateView):
    template_name = 'product/index.html'
    extra_context = {
        'products': Product.objects.all(),
        'category': Category.objects.all().filter(ref_category=None),
    }


class ProductDetailsView(generic.DetailView):
    template_name = 'product/detail.html'
    model = Product
    context_object_name = 'product_details'


class ProductCardView(generic.DetailView):
    template_name = 'product/card.html'
    model = Product
    context_object_name = 'product_card'


# class CategoryIndexView(generic.TemplateView):
#     template_name = 'product/category_index.html'
#     extra_context = {
#         'products': Product.filter_by_category(),
#         'category': Category.objects.all().filter(ref_category=None),
#     }


class CategoryView(View):

    def get(self, request, *args, **kwargs):
        category_id = kwargs['id']
        cat = Category.objects.get(id=category_id)
        cats = []
        for c in Category.objects.all():
            if c.ref_category == cat:
                cats.append(c)
        # print(category_id, cats)
        products = []
        for product in Product.objects.all():
            for x in cats:
                if product.category == x:
                    products.append(product)

        # products = Product.objects.all().filter(category__in=cats)
        # print('p:',products)
        category = Category.objects.all().filter(ref_category=None)
        return render(request, 'product/category_index.html', {'products': products, 'category': category})


class CategoryCardView(generic.DetailView):
    template_name = 'product/category_panel.html'
    model = Category
    context_object_name = 'category'
