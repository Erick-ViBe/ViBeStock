from django.apps import AppConfig
from django.utils import timezone


class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vibestock.products'

    def ready(self):
        from background_task.models import Task
        from datetime import datetime, time
        from vibestock.tasks.daily_update_product import task as daily_update_product
        today_date = datetime.now()

        today_datetime = timezone.make_aware(
            datetime.combine(today_date, time(hour=12, minute=0)),
            timezone=timezone.utc
        )

        daily_update_product(
          schedule=today_datetime,
            repeat=Task.DAILY,
        )
