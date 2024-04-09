from django.apps import AppConfig


class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vibestock.products'

    def ready(self):
        from background_task.models import Task
        from datetime import datetime, time
        from vibestock.tasks.daily_update_product import task as daily_update_product

        today_date = datetime.now()
        daily_update_product(
            schedule=datetime.combine(today_date, time(hour=12, minute=0)),
            repeat=Task.DAILY,
        )
