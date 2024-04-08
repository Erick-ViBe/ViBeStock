from django.core.mail import send_mail
from django.conf import settings

from datetime import timedelta

from background_task import background

from vibestock.products import models


@background(schedule=10)
def task(product_id):
    product = models.Product.objects.get(id=product_id)
    product.status = 'EXPIRED'
    product.save()

    send_mail(
        f'Alert! Your product {product.name} has expired',
        f'''
        Your product expires today.

            Name: {product.name}
            Status: {product.status.lower().replace('_', ' ')}
            Description: {product.description}
            Stock: {product.stock}
            Expiration Date: {product.expiration_date}
        ''',
        settings.SENDER_EMAIL,
        [product.user.email]
    )
