from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Discount, Category, Product


def validate_positive_value(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )


def validate_percent_lesser_hundred(value):
    if Discount.type == '%':
        if value >= 100:
            raise ValidationError(
                _('discount value in percent must be lesser 100')
            )


def validate_discount_percent_lesser_max_value(value):
    if Discount.type == '%':
        if value > Discount.max_value:
            raise ValidationError(
                _('discount value cant be greater than discount max value')
            )


