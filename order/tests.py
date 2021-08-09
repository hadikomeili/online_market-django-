from django.test import TestCase
from datetime import datetime, timedelta
from .models import *
from customer.models import *
from product.models import *

# Create your tests here.


class TestOrderItemModel(TestCase):

    def setUp(self) -> None:
        self.cat1 = Category.objects.create(name='cat')
        self.cat1.save()
        self.discount1 = Discount.objects.create(type='cash', value=1000, start_time=datetime.now().date(),
                                                 expire_time=(datetime.now().date() + timedelta(days=5)))
        self.discount1.save()
        self.p1 = Product.objects.create(name='test_p1', company_brand='test_brand', category=self.cat1,
                                         discount=self.discount1, price=15000, inventory=120,
                                         specifications='international product')
        self.p1.save()
        self.customer1 = Customer.objects.create(phone='099912345633', email='te2325@t1321.com', password='test632111',
                                                 birthday=datetime.now().date(), username='09991234563')
        self.customer1.save()
        self.cart1 = Cart.objects.create(customer=self.customer1)
        self.cart1.save()
        self.order_item1 = OrderItem.objects.create(product=self.p1, product_number=2, cart=self.cart1)

    def test_create_order_item(self):
        self.order_item1.save()

        self.assertIn(self.order_item1, OrderItem.objects.all())
        self.assertIn(self.order_item1, OrderItem.objects.archive())
        self.assertIsInstance(self.order_item1, OrderItem)

    def test_deleted_order_item(self):
        self.order_item1.deleted = True
        self.order_item1.save()

        self.assertIn(self.order_item1, OrderItem.objects.archive())
        self.assertNotIn(self.order_item1, OrderItem.objects.all())
        self.assertNotIn(self.order_item1, OrderItem.objects.filter())

    def test_order_item_foreign_key(self):
        self.order_item1.save()

        self.assertIsInstance(self.order_item1.cart, Cart)

    def test_order_item_number_positive(self):
        self.order_item1.save()

        self.assertTrue(self.order_item1.product_number >= 1)

    def test_order_item_status_method(self):
        self.p1.inventory = 100
        self.p1.save()
        self.order_item1.product_number = 50
        self.order_item1.save()

        self.assertEqual(self.order_item1.specify_order_item_status(), 'Available in inventory')

    def test_decrease_methode(self):
        self.p1.inventory = 100
        self.p1.save()
        self.order_item1.product_number = 50
        self.order_item1.save()
        self.order_item1.decrease_from_inventory()

        self.assertEqual(self.order_item1.product.inventory, 50)

    def test_increase_methode(self):
        self.p1.inventory = 100
        self.p1.save()
        self.order_item1.product_number = 40
        self.order_item1.save()
        self.order_item1.decrease_from_inventory()

        self.assertEqual(self.order_item1.product.inventory, 60)
        self.order_item1.increase_to_inventory()
        self.assertEqual(self.order_item1.product.inventory, 100)

    def test_checking_method(self):
        self.p1.inventory = 100
        self.p1.save()
        self.order_item1.product_number = 40
        self.order_item1.save()

        self.assertEqual(self.order_item1.check_inventory(), True)

    def test_checking_method2(self):
        self.p1.inventory = 25
        self.p1.save()
        self.order_item1.product_number = 40
        self.order_item1.save()

        self.assertEqual(self.order_item1.check_inventory(), 'Inventory shortage for this numbers!')

    def test_checking_method3(self):
        self.p1.inventory = 0
        self.p1.save()
        self.order_item1.product_number = 40
        self.order_item1.save()

        self.assertEqual(self.order_item1.check_inventory(), 'This product is unavailable!')

    def test_checking_method4(self):
        self.p1.inventory = 15
        self.p1.save()
        self.order_item1.product_number = -10
        self.order_item1.save()

        self.assertEqual(self.order_item1.check_inventory(), 'This number is incorrect!')

    def test_filter_by_cart_method(self):
        self.p2 = Product.objects.create(name='test_p2', company_brand='test_brand', category=self.cat1,
                                         discount=self.discount1, price=20000, inventory=100,
                                         specifications='international test product')
        self.p2.save()
        self.order_item2 = OrderItem.objects.create(product=self.p2, product_number=1, cart=self.cart1)
        self.order_item2.save()
        items = OrderItem.filter_by_cart(self.cart1)

        for item in items:
            self.assertEqual(item.cart, self.cart1)

    def test_final_cart_price_method(self):
        self.discount1.save()
        self.order_item1.save()
        self.p2 = Product.objects.create(name='test_p2', company_brand='test_brand', category=self.cat1,
                                         discount=self.discount1, price=10000, inventory=100,
                                         specifications='international test product')
        self.p2.save()
        self.order_item2 = OrderItem.objects.create(product=self.p2, product_number=1, cart=self.cart1)
        self.order_item2.save()

        print(OrderItem.final_cart_price(self.cart1))
        self.assertEqual(OrderItem.final_cart_price(self.cart1), 40000)

    def test_calculate_order_item_price_method(self):
        self.order_item1.save()

        print(self.order_item1.calculate_order_item_price())
        self.assertEqual(self.order_item1.calculate_order_item_price(), 30000)

    def test_logic_delete_method(self):
        self.order_item1.logic_delete()

        self.assertEqual(self.order_item1.deleted, True)
        self.assertNotEqual(self.order_item1.delete_timestamp, None)


class TestCartModel(TestCase):

    def setUp(self) -> None:
        self.cat1 = Category.objects.create(name='cat_test')
        self.cat1.save()
        self.discount1 = Discount.objects.create(type='cash', value=1000, start_time=datetime.now().date(),
                                                 expire_time=(datetime.now().date() + timedelta(days=5)))
        self.discount1.save()
        self.p1 = Product.objects.create(name='test_p1', company_brand='test_brand', category=self.cat1,
                                         discount=self.discount1, price=15000, inventory=120,
                                         specifications='international product')
        self.p1.save()
        self.customer1 = Customer.objects.create(phone='099912345633', email='te2325@t1321.com', password='test632111',
                                                 birthday=datetime.now().date(), username='09991234563')
        self.customer1.save()
        self.cart1 = Cart.objects.create(customer=self.customer1)
        # self.cart1.save()
        # self.order_item1 = OrderItem.objects.create(product=self.p1, product_number=2, cart=self.cart1)
        # self.order_item1.save()

    def test_create_cart_all(self):
        self.cart1.save()

        self.assertIn(self.cart1, Cart.objects.all())

    def test_create_cart_archive(self):
        self.cart1.save()

        self.assertIn(self.cart1, Cart.objects.archive())

    def test_create_cart_instance(self):
        self.cart1.save()

        self.assertIsInstance(self.cart1, Cart)

    def test_deleted_cart_all(self):
        self.cart1.deleted = True
        self.cart1.save()

        self.assertNotIn(self.cart1, Cart.objects.all())

    def test_deleted_cart_filter(self):
        self.cart1.deleted = True
        self.cart1.save()

        self.assertNotIn(self.cart1, Cart.objects.filter())

    def test_deleted_cart_archive(self):
        self.cart1.deleted = True
        self.cart1.save()

        self.assertIn(self.cart1, Cart.objects.archive())

    def test_cart_model_foreign_key(self):
        self.cart1.save()

        self.assertIsInstance(self.cart1.customer, Customer)

    def test_logic_delete_method(self):
        self.cart1.logic_delete()

        self.assertEqual(self.cart1.deleted, True)
        self.assertNotEqual(self.cart1.delete_timestamp, None)