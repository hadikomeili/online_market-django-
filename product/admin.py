from django.contrib import admin
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Register your models here.


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = []

    def clean(self):
        price = self.cleaned_data.get('price')
        inventory = self.cleaned_data.get('inventory')
        discount = self.cleaned_data.get('discount')
        discount_value = discount.value
        discount_type = discount.type
        if price < 0:
            raise ValidationError(_('price must be a positive value!'))
        elif inventory < 0:
            raise ValidationError(_('inventory must be a positive value!'))
        elif discount_type == '$':
            if discount_value > price:
                raise ValidationError(_('price must be greater than discount!'))
        return self.cleaned_data


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'discount', 'inventory')


admin.site.register(Product, ProductAdmin)


class DiscountForm(forms.ModelForm):

    class Meta:
        model = Discount
        exclude = []

    def clean(self):
        type = self.cleaned_data.get('type')
        value = self.cleaned_data.get('value')
        max_value = self.cleaned_data.get('max_value')
        start_time = self.cleaned_data.get('start_time')
        expire_time = self.cleaned_data.get('expire_time')
        if start_time > expire_time:
            raise ValidationError(_('expire time must be greater than start time!'))
        elif type == '%':
            if value > 100 or value < 0:
                raise ValidationError(_('percent value must be between 0 and 100!'))
            if value > max_value:
                raise ValidationError(_('percent value must be lesser than maximum value!'))
        elif type == '$':
            if value < 0:
                raise ValidationError(_('value can not be negative!'))



        return self.cleaned_data


class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = ('value', 'type', 'max_value', 'specify_discount_status')


admin.site.register(Discount, DiscountAdmin)


admin.site.register(Category)
