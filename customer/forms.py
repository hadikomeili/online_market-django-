from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .validators import *
from django.utils.translation import gettext as _


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['deleted', 'create_timestamp', 'modify_timestamp', 'delete_timestamp', 'date_joined',
                   'is_active', 'is_staff']

    phone = forms.CharField(max_length=11, validators=[customer_phone_validator, customer_phone_length_validator,
                                                       customer_phone_start_validator, customer_input_string_validator],
                            label=_('phone'), help_text=_('enter  phone number'))
    national_code = forms.CharField(max_length=10, label=_('national code'), help_text=_('enter national code'),
                                    validators=[customer_national_code_validator, customer_input_string_validator,
                                                customer_national_code_length_validator])


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['deleted']
        owner = forms.ModelChoiceField(queryset=Address.objects.all(), label=_('customer name'),
                                       help_text=_('specify customer'),
                                       validators=[address_owner_is_instance_customer_model], disabled=True)
        title = forms.CharField(max_length=25, label=_('address title'), help_text=_('enter title for this address'),
                                validators=[customer_input_string_validator, address_title_is_title_validator])
        country = forms.CharField(max_length=30, label=_('country name'), help_text=_('enter country name'),
                                  validators=[customer_input_string_validator, address_title_is_title_validator])
        state = forms.CharField(max_length=50, label=_('state name'), help_text=_('enter state name'),
                                validators=[customer_input_string_validator, address_title_is_title_validator])
        city = forms.CharField(max_length=50, label=_('city name'), help_text=_('enter city name'),
                               validators=[customer_input_string_validator, address_title_is_title_validator])
        village = forms.CharField(max_length=50, label=_('village name'), help_text=_('enter village name'),
                                  validators=[customer_input_string_validator, address_title_is_title_validator])
        post_code = forms.CharField(max_length=10, label=_('post code'), help_text=_('enter post code'),
                                    validators=[customer_input_string_validator, address_post_code_validator,
                                                address_post_code_length_validator])