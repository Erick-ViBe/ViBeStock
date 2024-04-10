from django.db.models import Manager
from django.conf import settings

from datetime import date, datetime, time, timedelta

from vibestock.tasks.send_expiration_alert import task as send_expiration_alert
from vibestock.tasks.send_expired_product import task as send_expired_product


class ProductManager(Manager):
    def create(self, **obj_data):
        expiration_date = obj_data.get('expiration_date')
        today = date.today()
        difference_days = (expiration_date - today).days

        user_expiration_alerts = obj_data['user'].expiration_alerts.all().values_list('number_of_days')
        expiration_alerts = [ day[0] for day in user_expiration_alerts ] + settings.DEFAULT_PRODUCT_EXPIRATION_ALERT_DAYS

        if difference_days == 0:
            obj_data['status'] = 'EXPIRED'
        elif difference_days > 0:
            max_expiration_alert_day = max(expiration_alerts)
            if difference_days <= max_expiration_alert_day:
                obj_data['status'] = 'TO_EXPIRE'
            obj_data['days_to_expire'] = difference_days
        elif difference_days < 0:
            obj_data['status'] = 'EXPIRED'
            obj_data['expired_days'] = abs(difference_days)

        create_response = super().create(**obj_data)

        send_expired_product(
            str(create_response.id),
            schedule=datetime.combine(expiration_date, time(hour=12))
        )
        print('Expired product alert created: {create_response.id} - {expiration_date}')

        for expiration_alert in expiration_alerts:
            if (expiration_alert < difference_days):
                date_to_send_expiration_alert = expiration_date - timedelta(days=expiration_alert)
                send_expiration_alert(
                    str(create_response.id),
                    expiration_alert,
                    schedule=datetime.combine(date_to_send_expiration_alert, time(hour=12))
                )
                print('To expire product alert created: {create_response.id} - {date_to_send_expiration_alert}')

        return create_response
