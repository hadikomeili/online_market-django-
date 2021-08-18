from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .validators import *
from django.utils.translation import gettext as _


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ['deleted']

    subject = forms.CharField(label=_('subject'), help_text=_('enter message subject here'),
                              validators=[input_name_subject_text_validator], required=True)
    customer_name = forms.CharField(label=_('customer name'), help_text=_('enter your name here'),
                                    validators=[input_name_subject_text_validator], required=True)
    phone_number = forms.CharField(label=_('phone number'), help_text=_('enter your phone number here'),
                                   validators=[phone_number_length_validator, phone_number_is_digit_validator,
                                               phone_number_start_with_validator], required=True)
    email = forms.EmailField(label=_('email'), help_text=_('enter your email here'), required=True)
    message_text = forms.TextInput(attrs={'cols': '60', 'rows': '3'})