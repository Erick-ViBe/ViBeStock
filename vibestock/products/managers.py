from django.db.models import Manager
from django.conf import settings

from datetime import date


class ProductManager(Manager):
    def create(self, **obj_data):
        expiration_date = obj_data.get('expiration_date')
        today = date.today()
        difference_days = (expiration_date - today).days

        if difference_days == 0:
            obj_data['status'] = 'EXPIRED'
        elif difference_days > 0:
            user_expiration_alerts = obj_data['user'].expiration_alerts.all().values_list('number_of_days')
            max_expiration_alert_day = max([ day[0] for day in user_expiration_alerts ] + settings.DEFAULT_PRODUCT_EXPIRATION_ALERT_DAYS)
            if difference_days <= max_expiration_alert_day:
                obj_data['status'] = 'TO_EXPIRE'
            obj_data['days_to_expire'] = difference_days
        elif difference_days < 0:
            obj_data['status'] = 'EXPIRED'
            obj_data['expired_days'] = abs(difference_days)

        return super().create(**obj_data)
