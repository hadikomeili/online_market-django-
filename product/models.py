from django.db import models
from datetime import datetime

from django.utils.translation import gettext as _

from core.models import BaseModel


# Create your models here.

class Category(BaseModel):
    """
    a model for categorize products
    """
    name = models.CharField(verbose_name=_('english name'), max_length=30, help_text=_('enter name in english'),
                            null=False, blank=False)
    name_fa = models.CharField(verbose_name=_('farsi name'), max_length=30, help_text=_('enter name in farsi'),
                               null=False, blank=False)
    ref_category = models.ForeignKey('self', verbose_name=_('parent category'), help_text=_('specify parent category'),
                                     null=True, blank=True, on_delete=models.SET_NULL)
    image = models.FileField(verbose_name=_('category image'), help_text=_('upload image of category'), null=True,
                             blank=True, upload_to='product/category/images/')
    level = models.IntegerField(verbose_name=_('category level'), help_text=_('specify level of self relation'),
                                null=True, blank=True, default=0, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.ref_category is not None:
            self.level = self.ref_category.level + 1
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        if self.ref_category is None:
            name = f'{self.name}'
        else:
            name = f'{self.ref_category}-{self.name}'
        return f'{name}'


class Discount(BaseModel):
    """
    a model for arrange and manage discount on product model
    """
    type = models.CharField(verbose_name=_('discount type'), help_text=_('specify type of discount'), null=False,
                            blank=False, choices=[('%', _('percent')), ('$', _('cash'))], max_length=15)
    value = models.IntegerField(verbose_name=_('discount value'), help_text=_('specify discount value'), null=True,
                                blank=True, default=0)
    max_value = models.IntegerField(verbose_name=_('maximum value'), help_text=_('specify maximum value'),
                                    null=True, blank=True)

    start_time = models.DateField(verbose_name=_('discount start time'),
                                  help_text=_('specify start time'), null=False, blank=False)
    expire_time = models.DateField(verbose_name=_('discount expire time'),
                                   help_text=_('specify expire time'), null=False, blank=False)

    def specify_discount_status(self):
        """
        method for specify discounts status in product models
        """
        if datetime.now().date() > self.expire_time:
            status = 'Expired'
        elif datetime.now().date() < self.start_time:
            status = 'Waiting'
        else:
            status = 'Active'
        return status

    def __str__(self):
        if self.specify_discount_status() == 'Active':
            return f'{self.value}{self.type}'
        else:
            return '-'


class Product(BaseModel):
    """
    a model for manage products
    """
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
                                 null=False, blank=False, on_delete=models.SET(0))
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
        """
        method for calculate final price of product based on discount type and value
        :return: union[int, float]
        """
        final_price = self.price
        if self.discount.specify_discount_status() == 'Active':
            if self.discount.type == '$':
                final_price = self.price - self.discount.value
            elif self.discount.type == '%':
                if self.discount.value != 0:
                    final_price = self.price - ((self.discount.value / 100) * self.price)
                else:
                    pass
        return int(final_price)

    def inventory_status(self):
        """
        method for specify inventory status in models
        :return: str
        """

        if self.inventory > 0:
            status = _('Available')
        else:
            status = _('Unavailable')
        return status

    @classmethod
    def filter_by_category(cls, category_id):
        """
        method for filter products based on category
        :param category_id: int
        :return: objects
        """
        res = cls.objects.filter(category=category_id)
        return res

    def __str__(self):
        return f'{self.name}'


