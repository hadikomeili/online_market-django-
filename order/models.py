from django.db import models
from datetime import datetime

from django.utils.translation import gettext as _

from core.models import BaseModel
from customer.models import Customer
from product.models import Product


# Create your models here.


class Cart(BaseModel):
    """
    a model for customer Cart consist of order items
    """
    customer = models.OneToOneField(Customer, verbose_name=_('customer'),
                                    help_text=_('specify owner customer for cart'),
                                    null=False, blank=False)

    # status = models.CharField(verbose_name=_('cart status'), help_text=_('display cart status'), null=False,
    #                           blank=False, choices=[('W', _('waiting'), ('F', _('final cart')))])

    def specify_cart_status(self):
        """
        method for specify cart status in order models
        """
        pass


class OrderItem(BaseModel):
    """
    a model for each product that add to cart
    """
    product = models.ForeignKey(Product, verbose_name=_('selected product'),
                                help_text=_('select product for add to your Cart'), on_delete=models.RESTRICT,
                                null=False, blank=False)
    product_number = models.IntegerField(verbose_name=_('numbers'), help_text=_('specify number of selected product'),
                                         null=False, blank=False, default=1)
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), help_text=_('specify cart'), null=False, blank=False,
                             on_delete=models.CASCADE)

    def specify_order_item_status(self):
        """
        method for specify order_item status in order models
        """
        if self.product_number <= self.product.inventory:
            status = _('Available in inventory')
        else:
            status = _('Inventory shortage')

        return status
