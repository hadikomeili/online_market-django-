from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from .models import *
from .forms import *


# Create your views here.

# -------------------- FormViews --------------------- #


class OrderItemFormView(generic.FormView):
    template_name = 'order/order_item_form.html'
    form_class = OrderItemForm

    success_url = reverse_lazy('order:add_order_item_form')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# ------------------- Views ----------------------- #


class OrderItemCardView(generic.DetailView):
    """
    View class for card view each order item
    """
    template_name = 'order/order_item_card.html'
    model = OrderItem
    context_object_name = 'order_item_card'


class OrderItemIndexView(generic.TemplateView):
    """
    View class for display all order items
    """
    template_name = 'order/all_order_items.html'
    extra_context = {
        'order_items': OrderItem.objects.all()
    }


class OrderItemDetailView(generic.DetailView):
    """
    View class for display details of an order item
    """
    template_name = 'order/order_item_detail.html'
    model = OrderItem
    context_object_name = 'order_item_detail'


