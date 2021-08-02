from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _

from core.models import BaseModel


# Create your models here.

class Category(BaseModel):
    name = models.CharField(verbose_name=_('english name'), max_length=30, help_text=_('enter name in english'),
                            null=False, blank=False)
    name_fa = models.CharField(verbose_name=_('farsi name'), max_length=30, help_text=_('enter name in farsi'),
                               null=False, blank=False)
    ref_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.ref_category is not None:
            str = f'{self.ref_category}-{self.name}'
        else:
            str = f'{self.name}'

        return str


class Discount(BaseModel):
    type = models.CharField(verbose_name=_('discount type'), help_text=_('specify type of discount'), null=False,
                            blank=False, choices=[('%', _('percent')), ('$', _('cash'))], max_length=15)
    value = models.IntegerField(verbose_name=_('discount value'), help_text=_('specify discount value'), null=True,
                                blank=True, default=0)
    max_value = models.IntegerField(verbose_name=_('maximum value'), help_text=_('specify maximum value'),
                                    null=True, blank=True)     #????????????????????????????????????????????????????

    start_time = models.DateField(verbose_name=_('discount start time'),
                                  help_text=_('specify start time'), null=False, blank=False)
    expire_time = models.DateField(verbose_name=_('discount expire time'),
                                   help_text=_('specify expire time'), null=False, blank=False)

    def specify_discount_status(self):
        if datetime.now().date() > self.expire_time:
            status = 'Expired'
        elif datetime.now().date() < self.start_time:
            status = 'Waiting'
        else:
            status = 'Active'
        return status

    def __str__(self):
        return f'{self.value}{self.type} => {self.specify_discount_status()} '


class Product(BaseModel):
    name = models.CharField(verbose_name=_('english name'), max_length=50, help_text=_('enter name in english'),
                            null=False, blank=False)
    name_fa = models.CharField(verbose_name=_('farsi name'), max_length=50, help_text=_('enter name in farsi'),
                               null=False, blank=False)
    company_brand = models.CharField(verbose_name=_('english company brand'), max_length=30,
                                     help_text='enter company brand name in english', null=False, blank=False)
    company_brand_fa = models.CharField(verbose_name=_('farsi company brand'), max_length=30,
                                        help_text='enter company brand name in farsi', null=False, blank=False)
    category = models.ForeignKey(Category, verbose_name=_('category'), help_text=_('specify category'),
                                 on_delete=models.RESTRICT, null=False, blank=False)
    discount = models.ForeignKey(Discount, verbose_name=_('discount'), help_text=_('specify discount'),
                                 null=False, blank=False, on_delete=models.RESTRICT)
    price = models.IntegerField(verbose_name=_('price'), help_text=_('enter price'), null=False, blank=False)
    inventory = models.IntegerField(verbose_name=_('inventory'), help_text=_('specify product inventory'),
                                    null=False, blank=False)
    image = models.FileField(verbose_name=_('product image'), help_text=_('upload image of product'), null=True,
                             blank=True, upload_to='product/images/')
    specifications = models.CharField(verbose_name=_('english product specifications'), null=True, blank=True,
                                      help_text=_('enter product specifications in english'), max_length=100)
    specifications_fa = models.CharField(verbose_name=_('farsi product specifications'), null=True, blank=True,
                                         help_text=_('enter product specifications in farsi'), max_length=100)

    def calculate_final_price(self):
        final_price = self.price
        if self.discount.specify_discount_status() == 'Active':
            if self.discount.type == '$':
                final_price = self.price - self.discount.value
            elif self.discount.type == '%':
                if self.discount.value != 0:
                    final_price = self.price - ((self.discount.value / 100) * self.price)
                else:
                    pass
        return final_price

    def inventory_status(self):

        if self.inventory > 0:
            status = _('Available')
        else:
            status = _('Unavailable')
        return status

    def __str__(self):
        return f'{self.id}# {self.name}: {self.price} - {self.inventory_status()}'
