from django.db import models


# Create your models here.


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        return super().get_queryset()


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
