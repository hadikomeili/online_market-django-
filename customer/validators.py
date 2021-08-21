from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext as _


def customer_input_string_validator(inp: str):
    if not isinstance(inp, str):
        raise ValidationError(_('input must be string!'))


def customer_name_is_title_validator(name: str):
    if not name.istitle():
        raise ValidationError(_('name must be Title!'))


def customer_phone_validator(phone: str):
    if not phone.isdigit():
        raise ValidationError(_('phone must be all digits!'))


def customer_phone_length_validator(phone: str):
    if not len(phone) == 11:
        raise ValidationError(_('phone must be 11 characters!'))


def customer_phone_start_validator(phone: str):
    if not phone.startswith('09'):
        raise ValidationError(_('phone must be start with 09 !'))


def customer_national_code_validator(n_code: str):
    if not n_code.isdigit():
        raise ValidationError(_('national code must be all digits!'))


def customer_national_code_length_validator(n_code: str):
    if not len(n_code) == 10:
        raise ValidationError(_('national code must be 10 characters!'))


def customer_birthday_validator(birthday: datetime):
    if not isinstance(birthday, datetime):
        raise ValidationError(_('phone must be date!'))

# ----------- address ------------- #


def address_post_code_validator(p_code: str):
    if not p_code.isdigit():
        raise ValidationError(_('post code must be all digits!'))


def address_post_code_length_validator(p_code: str):
    if not len(p_code) == 10:
        raise ValidationError(_('post code must be 10 characters!'))


def address_title_is_title_validator(name: str):
    if not name.istitle():
        raise ValidationError(_('Title inputs must be Title!'))


def address_owner_is_instance_customer_model(owner: Customer):
    if not isinstance(owner, Customer):
        raise ValidationError(_('owner must be one of registered customers!'))


