from django.db import models
from datetime import datetime

from django.utils.translation import gettext as _

from core.models import User, BaseModel
# Create your models here.


class Customer(User):
    """
    a model for customer in this project
    """
    class Meta:
        verbose_name = 'customer'
    pass


class Address(BaseModel):
    """
    a model for add customer addresses
    """
    customer = models.ForeignKey(Customer, verbose_name=_('customer name'), help_text=_('specify customer'),
                                 null=False, blank=False, on_delete=models.CASCADE)
    country = models.CharField(verbose_name=_('country name'), help_text=_('enter country name'), null=False,
                               blank=False, default='Iran', max_length=30)
    state = models.CharField(verbose_name=_('state name'), help_text=_('enter state name'), null=False, blank=False
                             , max_length=50)
    city = models.CharField(verbose_name=_('city name'), help_text=_('enter city name'), null=False, blank=False,
                            max_length=50)
    village = models.CharField(verbose_name=_('village name'), help_text=_('enter village name'), null=True,
                               blank=True, max_length=50)
    rest_of_address = models.TextField(verbose_name=_('rest of address'), help_text=_('enter rest of address'),
                                       null=False, blank=False)
    post_code = models.CharField(verbose_name=_('post code'), help_text=_('enter post code'), null=True,
                                 blank=True, max_length=10)