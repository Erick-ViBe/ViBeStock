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
    stock = models.SmallIntegerField()
    expiration_date = models.DateField()
    alert_activated = models.BooleanField(default=False)
    days_to_activate_alert = models.SmallIntegerField(default=0)
    days_since_alert_activated = models.SmallIntegerField(default=0)

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
