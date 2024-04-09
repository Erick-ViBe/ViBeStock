from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import date

from vibestock.products.models import Product, ExpirationAlerts


def sample_user(email='test@email.com', password='testpassword'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelsTests(TestCase):

    def test_product(self):
        """ Test the product creation and str """
        product = Product.objects.create(
            user=sample_user(),
            name='Product name',
            description='Product description',
            stock=123,
            expiration_date=date(2024, 5, 5)
        )

        self.assertIsNotNone(product.id)
        self.assertEqual(str(product), product.name)

    def test_expiration_alert(self):
        """ Test the expiration alert creation and str """
        expiration_alert = ExpirationAlerts.objects.create(
            user=sample_user(),
            number_of_days=15,
        )

        self.assertIsNotNone(expiration_alert.id)
        self.assertEqual(str(expiration_alert), f'Alert in {expiration_alert.number_of_days} days')
