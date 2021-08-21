from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _

from core.models import BaseModel
from customer.models import Customer, Address
from product.models import Product


# Create your models here.


class Cart(BaseModel):
    """
    a model for customer Cart consist of order items
    """
    customer = models.ForeignKey(Customer, verbose_name=_('customer'),
                                 help_text=_('specify owner customer for cart'),
                                 null=True, blank=True, on_delete=models.PROTECT)

    status = models.CharField(verbose_name=_('cart status'), help_text=_('display cart status'), max_length=20,
                              blank=False, null=False, choices=[('WA', _('waiting')), ('PD', _('paid'))],
                              default='WA')
    final_price = models.IntegerField(verbose_name=_('final price'), help_text=_('final cart price'),
                                    null=True, blank=True)
    order_status = models.CharField(verbose_name=_('customer order status'), help_text=_('display status of order'),
                                    blank=False, null=False,
                                    choices=[('NW', _('new')), ('SN', _('send')), ('CA', _('cancel'))],
                                    default='NW', max_length=20)
    order_address = models.ForeignKey(Address, verbose_name=_('customer address'),
                                      help_text=_('specify address for send order'),
                                      null=True, blank=True, on_delete=models.PROTECT)

    def order_date(self):
        return self.create_timestamp.date()

    def address_by_customer(self):
        addresses = Address.objects.filter(owner=self.customer)
        return addresses

    def change_order_status_to_send(self):
        """
        method for change order status to SN
        """
        self.order_status = 'SN'
        return self.order_status

    def change_order_status_to_cancel(self):
        """
        method for change order status to SN
        """
        self.order_status = 'CA'
        return self.order_status

    def paid_cart(self):
        """
        method for change cart status to PD
        """
        self.status = 'PD'
        return self.status

    def cart_price(self):
        """
        method for calculate cart price
        """
        items = OrderItem.objects.filter(cart__customer=self.customer)
        all_items = items.filter(cart__status='WA')
        price = 0
        for item in all_items:
            price += item.product.calculate_final_price() * item.product_number
        return int(price)

    @classmethod
    def cart_history(cls):
        return cls.objects.archive()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        p = self.cart_price()
        self.final_price = p
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.customer}'


class OrderItem(BaseModel):
    """
    a model for each product that add to cart
    """
    product = models.ForeignKey(Product, verbose_name=_('selected product'),
                                help_text=_('select product for add to your Cart'), on_delete=models.CASCADE,
                                null=True, blank=True)
    product_number = models.IntegerField(verbose_name=_('numbers'), help_text=_('specify number of selected product'),
                                         null=False, blank=False, default=1)
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), help_text=_('specify cart'), null=True, blank=True,
                             on_delete=models.CASCADE, related_name='cart_orderitems',
                             related_query_name='customer_cart_orderitems')

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
            return int(order_item_price)
        else:
            return checking

    def decrease_from_inventory(self):
        """method for decrease number of products in order item from inventory after order finalization"""
        if self.check_inventory():
            self.product.inventory -= self.product_number
            self.product.save()

    def increase_to_inventory(self):
        """method for increase to inventory if order canceled"""
        self.product.inventory += self.product_number
        self.product.save()

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

    def __str__(self):
        return f'{self.product} : {self.product_number} for {self.cart}'
