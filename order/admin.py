from django.contrib import admin
from .models import *
from .forms import *
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Register your models here.


class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemForm
    list_display = ('product', 'product_number', 'cart')
    list_filter = ('cart', 'product')
    list_display_links = ('product', 'cart')
    list_editable = ('product_number',)
    ordering = ('product', 'product_number', 'cart')


admin.site.register(OrderItem, OrderItemAdmin)


class CartAdmin(admin.ModelAdmin):
    form = CartForm
    list_display = ('customer', 'status', 'final_price')
    list_filter = ('customer', 'status')
    list_display_links = ('customer',)
    list_editable = ('status',)
    ordering = ('customer', 'status')


admin.site.register(Cart, CartAdmin)


def logical_delete(modeladmin, request, queryset):
    queryset.update(deleted=True)


admin.site.add_action(logical_delete)
