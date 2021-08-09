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
                                    null=False, blank=False, on_delete=models.PROTECT)

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
                                help_text=_('select product for add to your Cart'), on_delete=models.PROTECT,
                                null=False, blank=False)
    product_number = models.IntegerField(verbose_name=_('numbers'), help_text=_('specify number of selected product'),
                                         null=False, blank=False, default=1)
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), help_text=_('specify cart'), null=True, blank=True,
                             on_delete=models.PROTECT)

    def specify_order_item_status(self):
        """
        method for specify order_item status in order models
        """
        if self.product_number <= self.product.inventory:
            status = _('Available in inventory')
        else:
            status = _('Inventory shortage')

        return status

    def check_inventory(self):
        if self.product_number >= 1:
            if self.product.inventory_status() == 'Available':
                if self.product_number <= self.product.inventory:
                    return True
                else:
                    return _('Inventory shortage for this numbers!')
            else:
                return _('This product is unavailable!')
        else:
            return _('This number is incorrect!')

    def calculate_order_item_price(self):
        """
        method for calculate order item final price
        """
        checking = self.check_inventory()
        if checking:
            order_item_price = self.product_number * self.product.calculate_final_price()
            return order_item_price
        else:
            return checking

    def decrease_from_inventory(self):
        """method for decrease number of products in order item from inventory after order finalization"""
        if self.check_inventory():
            self.product.inventory -= self.product_number

    def increase_to_inventory(self):
        """method for increase to inventory if order canceled"""
        self.product.inventory += self.product_number

    @classmethod
    def filter_by_cart(cls, cart):
        """
        method for filter order items based on cart
        """
        res = cls.objects.filter(cart=cart)
        return res

    @classmethod
    def final_cart_price(cls, cart):
        cart_items = cls.filter_by_cart(cart)
        cart_price = 0
        for item in cart_items:
            cart_price += item.calculate_order_item_price()
        return cart_price



