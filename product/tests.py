from django.test import TestCase
from datetime import datetime, timedelta
from .models import *


# Create your tests here.

class ProductModelTest(TestCase):

    def setUp(self) -> None:
        self.cat1 = Category.objects.create(name='test_cat')
        self.discount1 = Discount.objects.create(type='cash', value=1000, start_time=datetime.now(),
                                                 expire_time=(datetime.now() + timedelta(days=2)))
        self.p1 = Product.objects.create(name='test_p1', company_brand='test_brand', category=self.cat1,
                                         discount=self.discount1, price=15000, inventory=120,
                                         specifications='international product')

    def test_create_product(self):
        self.p1.save()

        self.assertIn(self.p1, Product.objects.all())

    def test_deleted_product(self):
        self.p1.deleted = True
        self.p1.save()

        self.assertIn(self.p1, Product.objects.archive())
        self.assertNotIn(self.p1, Product.objects.all())

    def test_foreign_key_category(self):
        self.p1.save()

        self.assertIn(self.p1.category, Category.objects.all())

    def test_foreign_key_discount(self):
        self.p1.save()

        self.assertIn(self.p1.discount, Discount.objects.all())

    def test_be_positive_price(self):
        self.p1.save()

        self.assertTrue(self.p1.price > 0)

    def test2_be_positive_price(self):
        self.p1.price = -100
        self.p1.save()

        self.assertFalse(self.p1.price > 0)

    def test_price_greater_than_discount(self):
        self.p1.save()

        if self.p1.discount.type == 'cash':
            self.assertTrue(self.p1.price > self.p1.discount.value)

        else:
            self.assertTrue(self.p1.discount.value < 100)

    def test_be_positive_inventory(self):
        self.p1.save()

        self.assertTrue(self.p1.inventory >= 0)


class CategoryModelTest(TestCase):

    def setUp(self) -> None:
        self.cat1 = Category.objects.create(name='test_cat')
        self.cat2 = Category.objects.create(name='test2_cat', ref_category=self.cat1)

    def test_create_category(self):
        self.cat1.save()

        self.assertIn(self.cat1, Category.objects.all())

    def test_deleted_category(self):
        self.cat1.deleted = True
        self.cat1.save()

        self.assertIn(self.cat1, Category.objects.archive())
        self.assertNotIn(self.cat1, Category.objects.all())

    def test_self_relation(self):
        self.cat1.save()
        self.cat2.save()

        self.assertIn(self.cat1, Category.objects.all())
        self.assertIn(self.cat2, Category.objects.all())
        self.assertIsInstance(self.cat1, Category)
        self.assertIsInstance(self.cat2, Category)


class DiscountModelTest(TestCase):

    def setUp(self) -> None:
        self.discount1 = Discount.objects.create(type='cash', value=1000, start_time=datetime.now(),
                                                 expire_time=(datetime.now() + timedelta(days=2)))
        self.discount2 = Discount.objects.create(type='percent', value=20, start_time=datetime.now(),
                                                 expire_time=(datetime.now() + timedelta(days=3)))

    def test_create_discount(self):
        self.discount1.save()

        self.assertIn(self.discount1, Discount.objects.all())

    def test_deleted_category(self):
        self.discount1.deleted = True
        self.discount1.save()

        self.assertIn(self.discount1, Discount.objects.archive())
        self.assertNotIn(self.discount1, Discount.objects.all())

    def test_be_positive_discount(self):
        self.discount1.save()
        self.discount2.save()

        self.assertTrue(self.discount1.value >= 0)
        self.assertTrue(self.discount2.value >= 0)

    def test2_be_positive_discount(self):
        self.discount2.value = -10
        self.discount2.save()

        self.assertFalse(self.discount2.value >= 0)

    def test_type_percent_lesser_than_hundred(self):
        self.discount2.save()

        if self.discount2.type == 'percent':
            self.assertTrue(self.discount2.value < 100)

    def test_expire_time_greater_than_start_time(self):
        self.discount2.save()

        self.assertTrue(self.discount2.expire_time > self.discount2.start_time)