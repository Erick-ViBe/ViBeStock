from django.db import models
from django.conf import settings

from vibestock.utils.models.base import BaseModel


class Product(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    stock = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.name
