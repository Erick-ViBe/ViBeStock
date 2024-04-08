from datetime import timedelta

from background_task import background


@background(schedule=timedelta(days=5))
def task(product_id, days_to_expire):
    print(f'Se va expirar el producto {product_id} en {days_to_expire} dias.')
