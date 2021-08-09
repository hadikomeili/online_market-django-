from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .validators import *
from django.utils.translation import gettext as _


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['deleted']

    product = forms.ModelChoiceField(queryset=Product.objects.all(), validators=[product_is_instance_product_model],
                                     label=_('product'), help_text=_('select intended product'))
    product_number = forms.IntegerField(validators=[product_number_int_validator, product_number_positive_validator],
                                        label=_('number'), help_text=_('specify number of product'))
    cart = forms.ModelChoiceField(queryset=Cart.objects.all(), validators=[cart_is_instance_cart_model], label=_('cart')
                                  , help_text=_('choose cart'))


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        exclude = ['deleted']

    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), validators=[customer_is_instance_customer_model],
                                      label=_('customer'), help_text=_('choose customer'))


