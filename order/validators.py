from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext as _


def product_number_int_validator(num: int):
    if not isinstance(num, int):
        raise ValidationError(_('number must be integer!'))


def product_number_positive_validator(num: int):
    if not num > 0:
        raise ValidationError(_('number must be greater than 0!'))


def product_is_instance_product_model(product: Product):
    if not isinstance(product, Product):
        raise ValidationError(_('product must be one of database products!'))


def cart_is_instance_cart_model(cart: Cart):
    if not isinstance(cart, Cart):
        raise ValidationError(_('cart must be one of database active carts!'))


def customer_is_instance_customer_model(customer: Customer):
    if not isinstance(customer, Customer):
        raise ValidationError(_('customer must be one of registered customers!'))


