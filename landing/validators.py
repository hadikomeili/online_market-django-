from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext as _


def phone_number_length_validator(num: str):
    if not len(num) == 11:
        raise ValidationError(_('phone number must be 11 character!'))


def phone_number_is_digit_validator(num: str):
    if not num.isdigit():
        raise ValidationError(_('phone number must be digits!'))


def phone_number_start_with_validator(num: str):
    if not num.startswith('09'):
        raise ValidationError(_('phone number must start with 09!'))


def input_name_subject_text_validator(text: str):
    if not text.isalnum():
        raise ValidationError(_('input must be alphabets or numbers!'))

