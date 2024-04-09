from django.db.models import F

from background_task import background

from vibestock.products import models


@background(schedule=10, remove_existing_tasks=True)
def task():
    models.Product.objects.filter(
        days_to_expire=0
    ).update(
        expired_days=F('expired_days')+1
    )
    models.Product.objects.filter(
        expired_days=0
    ).update(
        days_to_expire=F('days_to_expire')-1,
    )
