from django.test import TestCase
from datetime import datetime, timedelta
from .models import *
from core.models import User


# Create your tests here.


class CustomerModelTest(TestCase):

    def setUp(self) -> None:
        self.customer1 = Customer.objects.create(phone='09991234563', email='te2325@t1321.c2om', password='test632111',
                                                 birthday=datetime.now().date(), username='09991234563')
        self.customer3 = Customer.objects.create(phone='09001234567', email='test@t2.com', password='test6543210',
                                                 birthday=datetime.now().date(), username='09001234567')
        self.customer4 = Customer.objects.create(phone='09001234566', email='test@t4.com', password='test65432100',
                                                 birthday=datetime.now().date(), username='09001234566')

    def test_create_customer(self):
        self.customer1.save()

        self.assertIn(self.customer1, Customer.objects.all())

    def test_deleted_customer(self):
        self.customer1.deleted = True
        self.customer1.save()

        self.assertNotIn(self.customer1, Customer.objects.all())
        self.assertIn(self.customer1, Customer.objects.archive())

    def test_deleted_customer_filter(self):
        self.customer3.deleted = True
        self.customer3.save()

        self.assertNotIn(self.customer3, Customer.objects.filter())

    # def test_create_customer_without_phone(self):
    #     self.customer2 = Customer.objects.create(email='test@t.com', password='test654321',
    #                                              birthday=datetime.now().date())
    #     self.customer2.save()
    #
    #     self.assertNotIsInstance(self.customer2, Customer)

    # def test_phone_be_unique(self):
    #     self.customer1.save()
    #     self.customer2 = Customer.objects.create(phone='09991234563', email='test@t.com', password='test654321',
    #                                              birthday=datetime.now().date())
    #     self.customer2.save()
    #
    #     self.assertRaises(self.customer2, Customer)

    def test_parent(self):
        self.customer1.save()

        self.assertIsInstance(self.customer1, User)

    def test_calculate_age(self):
        self.customer1.save()

        self.assertTrue(self.customer1.calculate_age() >= 0)

    def test_customer_is_active(self):
        self.customer1.save()
        self.customer3.save()

        self.assertEqual(self.customer1.is_active, True)
        self.assertEqual(self.customer3.is_active, True)

    def test_customer_not_superuser(self):
        self.customer1.save()
        self.customer4.save()

        self.assertNotEqual(self.customer1.is_superuser, True)
        self.assertNotEqual(self.customer4.is_superuser, True)

    def test_customer_not_staff(self):
        self.customer1.save()
        self.customer4.save()

        self.assertNotEqual(self.customer1.is_staff, True)
        self.assertNotEqual(self.customer4.is_staff, True)

    # def test_birthday_type(self):
    #     self.customer1.birthday = datetime.now().time()
    #     self.customer1.save()
    #
    #     self.assertRaises(self.customer1, TypeError, )

    def test_logic_delete_method(self):
        self.customer1.logic_delete()

        self.assertEqual(self.customer1.deleted, True)
        self.assertNotEqual(self.customer1.delete_timestamp, None)


class AddressModelTest(TestCase):

    def setUp(self) -> None:
        self.customer1 = Customer.objects.create(phone='09991234563', email='te2325@t1321.c2om', password='test632111',
                                                 birthday=datetime.now().date(), username='09991234563')
        self.add1 = Address.objects.create(owner=self.customer1, state='tehran', city='tehran')

    def test_create_address(self):
        self.add1.save()

        self.assertIsInstance(self.add1, Address)

    def test_deleted_address(self):
        self.add1.deleted = True
        self.add1.save()

        self.assertNotIn(self.add1, Address.objects.all())
        self.assertIn(self.add1, Address.objects.archive())

    def test_deleted_address_filter(self):
        self.add1.deleted = True
        self.add1.save()

        self.assertNotIn(self.add1, Address.objects.filter())

    def test_delete_address_owner(self):
        self.customer1.deleted = True
        self.customer1.save()
        self.add1.save()

        self.assertNotIn(self.customer1, Customer.objects.all())
        self.assertIn(self.add1, Address.objects.all())

    def test_foreign_key_customer(self):
        self.add1.save()

        self.assertIn(self.add1.owner, Customer.objects.all())

    def test_logic_delete_method(self):
        self.add1.logic_delete()

        self.assertEqual(self.add1.deleted, True)
        self.assertNotEqual(self.add1.delete_timestamp, None)






