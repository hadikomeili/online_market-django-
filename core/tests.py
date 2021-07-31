from django.test import TestCase
from .models import TestModel

# Create your tests here.


class MyTestModelTest(TestCase):

    def setUp(self) -> None:
        self.ins1 = TestModel.objects.create()


    def test_create_instance(self):
        self.ins1.save()

        self.assertIn(self.ins1, TestModel.objects.all())
        self.assertIn(self.ins1, TestModel.objects.archive())


    def test_instance_deleted(self):
        self.ins1.deleted = True
        self.ins1.save()

        self.assertNotIn(self.ins1, TestModel.objects.all())

    def test_instance_in_archive(self):
        self.ins1.deleted = True
        self.ins1.save()

        self.assertIn(self.ins1, TestModel.objects.archive())

    def test2_instance_in_archive(self):
        self.ins1.save()

        self.assertIn(self.ins1, TestModel.objects.archive())