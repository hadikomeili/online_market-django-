from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _


# Create your models here.


class BaseManager(models.Manager):
    """
    create Base Manager for this project
    """

    def get_queryset(self):
        """
        over write get_queryset for personalization this for logical delete
        """
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        """
        rewrite get_queryset for access to all objects and data in this project
        """
        return super().get_queryset()


class BaseModel(models.Model):
    """
    create Base Model for this project
    """
    deleted = models.BooleanField(default=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)
    delete_timestamp = models.DateTimeField(default=None, null=True, blank=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def logic_delete(self):
        """
        create method for logical delete for this project
        """
        self.deleted = True
        self.delete_timestamp = datetime.now()
        self.save()


# ---------------------USER--------------------- #


class MyUserManager(UserManager):

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'phone'

    phone = models.CharField(verbose_name=_('phone'), max_length=11, unique=True)
    national_code = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=10, choices=[], blank=True)
    birthday = models.DateField(null=True, blank=True)

    objects = MyUserManager()


class TestModel(BaseModel):
    pass
