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
        'products': Product.objects.all()
    }

class ProductDetailsView(generic.DetailView):
    template_name = 'product/detail.html'
    model = Product
    context_object_name = 'product_details'

class ProductCardView(generic.DetailView):
    template_name = 'product/card.html'
    model = Product
    context_object_name = 'product_card'