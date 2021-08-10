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
    delete_timestamp = models.DateTimeField(default=None, null=True, blank=True, editable=False)

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

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)


# ---------------------USER--------------------- #


class MyUserManager(UserManager):

    use_in_migrations = True
    #
    # def _create_user(self, phone, username, password, **extra_fields):
    #     if not phone:
    #         raise ValueError('The given phone must be set')
    #     self.phone = phone
    #     user = self.model(phone=phone, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    #
    # def create_superuser(self, phone, password, username=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #
    #     return self._create_user(phone, username, password, **extra_fields)
    #
    # def create_user(self, phone, username=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(phone, username, password, **extra_fields)

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


class User(AbstractUser):
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['email']

    phone = models.CharField(verbose_name=_('phone'), help_text=_('enter phone number'), max_length=11, unique=True,
                             null=False, blank=False)
    national_code = models.CharField(verbose_name=_('national code'), help_text=_('enter national code'),
                                     max_length=10, blank=True, null=True)
    gender = models.CharField(verbose_name=_('gender'), help_text=_('specify your gender'), max_length=10,
                              choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    birthday = models.DateField(verbose_name=_('birthday'), help_text=_('specify birthday date'), null=True, blank=True)

    deleted = models.BooleanField(default=False)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)
    delete_timestamp = models.DateTimeField(default=None, null=True, blank=True, editable=False)

    objects = MyUserManager()

    def logic_delete(self):
        """
        create method for logical delete for this project
        """
        self.deleted = True
        self.delete_timestamp = datetime.now()
        self.save()


# ------------------TESTS---------------------#


class TestModel(BaseModel):
    pass


class TestUser(User):
    pass

