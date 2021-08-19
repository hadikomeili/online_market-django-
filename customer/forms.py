from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .validators import *
from django.utils.translation import gettext as _
from core.models import User


# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         exclude = ['deleted', 'create_timestamp', 'modify_timestamp', 'delete_timestamp', 'date_joined',
#                    'is_active', 'is_staff']
#
#     phone = forms.CharField(max_length=11, validators=[customer_phone_validator, customer_phone_length_validator,
#                                                        customer_phone_start_validator, customer_input_string_validator],
#                             label=_('phone'), help_text=_('enter  phone number'))
#     national_code = forms.CharField(max_length=10, label=_('national code'), help_text=_('enter national code'),
#                                     validators=[customer_national_code_validator, customer_input_string_validator,
#                                                 customer_national_code_length_validator])


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['deleted', 'owner']
        # read_only_fields = ['owner']
    # owner = forms.ModelChoiceField(queryset=Address.objects.all(), label=_('customer name'),
    #                                help_text=_('specify customer'),
    #                                validators=[address_owner_is_instance_customer_model], required=False, disabled=True)
    title = forms.CharField(max_length=25, label=_('address title'), help_text=_('enter title for this address'),
                            validators=[customer_input_string_validator, address_title_is_title_validator])
    country = forms.CharField(max_length=30, label=_('country name'), help_text=_('enter country name'),
                              validators=[customer_input_string_validator, address_title_is_title_validator])
    state = forms.CharField(max_length=50, label=_('state name'), help_text=_('enter state name'),
                            validators=[customer_input_string_validator, address_title_is_title_validator])
    city = forms.CharField(max_length=50, label=_('city name'), help_text=_('enter city name'),
                           validators=[customer_input_string_validator, address_title_is_title_validator])
    village = forms.CharField(max_length=50, label=_('village name'), help_text=_('enter village name'), required=False,
                              validators=[customer_input_string_validator, address_title_is_title_validator])
    post_code = forms.CharField(max_length=10, label=_('post code'), help_text=_('enter post code'),
                                validators=[customer_input_string_validator, address_post_code_validator,
                                            address_post_code_length_validator])


class MyUserCreationForm(forms.ModelForm):
    phone = forms.CharField(max_length=11, validators=[customer_phone_validator, customer_phone_length_validator,
                                                       customer_phone_start_validator, customer_input_string_validator],
                            label=_('phone'), help_text=_('enter  phone number'))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_('Enter password'),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Customer
        fields = ('phone', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('password mismatch'))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = user.phone
        if commit:
            user.save()
        return user
