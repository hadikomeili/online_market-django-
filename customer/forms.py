from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .validators import *
from django.utils.translation import gettext as _
from core.models import User


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'national_code']

        # read_only_fields = ['phone', 'email']
    # phone = forms.CharField(max_length=11, validators=[customer_phone_validator, customer_phone_length_validator,
    #                         customer_phone_start_validator, customer_input_string_validator],
    #                         label=_('phone'), help_text=_('enter  phone number'),
    #                         disabled=True, required=False)
    first_name = forms.CharField(max_length=25, label=_('first name'), help_text=_('enter/change your first name'),
                                 validators=[customer_input_string_validator])
    last_name = forms.CharField(max_length=25, label=_('last name'), help_text=_('enter/change your last name'),
                                validators=[customer_input_string_validator])

    national_code = forms.CharField(max_length=10, min_length=10, label=_('national code'),
                                    help_text=_('enter/change national code'),
                                    validators=[customer_national_code_validator, customer_input_string_validator,
                                                customer_national_code_length_validator])
    # email = forms.EmailField(label=_('email'), help_text=_('enter/change your email'))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['deleted', 'owner']

    title = forms.CharField(max_length=25, label=_('address title'), help_text=_('enter/change title for this address'),
                            validators=[customer_input_string_validator, address_title_is_title_validator])
    country = forms.CharField(max_length=30, label=_('country name'), help_text=_('enter/change country name'),
                              validators=[customer_input_string_validator])
    state = forms.CharField(max_length=50, label=_('state name'), help_text=_('enter/change state name'),
                            validators=[customer_input_string_validator])
    city = forms.CharField(max_length=50, label=_('city name'), help_text=_('enter/change city name'),
                           validators=[customer_input_string_validator])
    village = forms.CharField(max_length=50, label=_('village name'), help_text=_('enter/change village name'),
                              validators=[customer_input_string_validator], required=False)
    post_code = forms.CharField(max_length=10, min_length=10, label=_('post code'),
                                help_text=_('enter/change post code'),
                                validators=[customer_input_string_validator, address_post_code_validator,
                                            address_post_code_length_validator], required=False)


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
