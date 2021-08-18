from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel

# Create your models here.


class Message(BaseModel):
    subject = models.CharField(max_length=50, verbose_name=_('subject'),
                               help_text=_('enter message subject here'), null=False, blank=False)
    customer_name = models.CharField(max_length=50, verbose_name=_('customer name'),
                                     help_text=_('enter your name here'), null=False, blank=False)
    phone_number = models.CharField(max_length=11, verbose_name=_('phone number'),
                                    help_text=_('enter your phone number here'), null=False, blank=False)
    email = models.CharField(max_length=50, verbose_name=_('email'), help_text=_('enter your email here'),
                             null=False, blank=False)
    message_text = models.TextField(max_length=200, verbose_name=_('message text'),
                                    help_text=_('enter your message here'), null=False, blank=False)

    def __str__(self):
        return f"{self.subject}: {self.customer_name}"
