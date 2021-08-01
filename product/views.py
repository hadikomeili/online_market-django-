from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import Http404, HttpResponse

from .models import *


# Create your views here.


class ProductDetailsView(generic.DetailView):
    template_name = 'product/detail.html'
    model = Product
    context_object_name = 'product_details'
