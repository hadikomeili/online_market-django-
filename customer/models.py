from django.db import models
from datetime import datetime

from django.utils.translation import gettext as _

from core.models import User, BaseModel


# Create your models here.


class Customer(User):
    """
    a model for customer in this project
    """
    national_code = models.CharField(verbose_name=_('national code'), help_text=_('enter national code'),
                                     max_length=10, blank=True, null=True)
    gender = models.CharField(verbose_name=_('gender'), help_text=_('specify your gender'), max_length=10,
                              choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)
    birthday = models.DateField(verbose_name=_('birthday'), help_text=_('specify birthday date'), null=True, blank=True)
    image = models.FileField(verbose_name=_('customer image'), help_text=_('upload your image'), null=True,
                             blank=True, upload_to='customer/images/')

    class Meta:
        verbose_name = 'customer'

    def calculate_age(self):
        """
        methode for calculate customer age
        :return: int
        """
        age = datetime.now().year - self.birthday.year
        return age

    @classmethod
    def filter_by_gender(cls, gen):
        """
        method for filter customers based on gender
        """
        res = cls.objects.filter(gender=gen)
        return res

    def customer_name(self):
        return self.__str__()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(BaseModel):
    """
    a model for add customer addresses
    """
    owner = models.ForeignKey(Customer, verbose_name=_('address owner'), help_text=_('specify owner'),
                              null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('address title'), help_text=_('enter title for this address'),
                             max_length=25, default='New')
    latitude = models.FloatField(verbose_name=_('latitude'), help_text=_('enter latitude'), null=True, blank=True)
    longitude = models.FloatField(verbose_name=_('longitude'), help_text=_('enter longitude'), null=True, blank=True)
    country = models.CharField(verbose_name=_('country name'), help_text=_('enter country name'), null=False,
                               blank=False, default='Iran', max_length=30)
    state = models.CharField(verbose_name=_('state name'), help_text=_('enter state name'), null=False, blank=False
                             , max_length=50)
    city = models.CharField(verbose_name=_('city name'), help_text=_('enter city name'), null=False, blank=False,
                            max_length=50)
    village = models.CharField(verbose_name=_('village name'), help_text=_('enter village name'), null=True,
                               blank=True, max_length=50)
    rest_of_address = models.TextField(verbose_name=_('rest of address'), help_text=_('enter rest of address'),
                                       null=False, blank=True)
    post_code = models.CharField(verbose_name=_('post code'), help_text=_('enter post code'), null=True,
                                 blank=True, max_length=10)

    @classmethod
    def filter_by_country(cls, country):
        """
        method for filter addresses based on country
        """
        res = cls.objects.filter(country=country)
        return res

    @classmethod
    def filter_by_state(cls, state):
        """
        method for filter addresses based on state
        """
        res = cls.objects.filter(state=state)
        return res

    @classmethod
    def filter_by_city(cls, city):
        """
        method for filter addresses based on city
        """
        res = cls.objects.filter(city=city)
        return res

    @classmethod
    def filter_by_owner(cls, owner):
        """
        method for filter addresses based on owner
        """
        res = cls.objects.filter(owner=owner)
        return res

    def __str__(self):
        return f'{self.title} in {self.city}#owner: {self.owner}'
