from django.db import models
from django.conf import settings

from vibestock.utils.models.base import BaseModel
from vibestock.products.managers import ProductManager


class Product(BaseModel):
    class ProductStatus(models.TextChoices):
        USABLE = 'USABLE'
        TO_EXPIRE = 'TO_EXPIRE'
        EXPIRED = 'EXPIRED'

    status = models.CharField(
        choices=ProductStatus.choices,
        default=ProductStatus.USABLE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    stock = models.SmallIntegerField()
    expiration_date = models.DateField()
    days_to_expire = models.SmallIntegerField(default=0)
    expired_days = models.SmallIntegerField(default=0)

    objects = ProductManager()

    def __str__(self):
        return self.name


class ExpirationAlerts(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expiration_alerts'
    )
    number_of_days = models.SmallIntegerField()

    def __str__(self):
        return f'Alert in {self.number_of_days} days'
