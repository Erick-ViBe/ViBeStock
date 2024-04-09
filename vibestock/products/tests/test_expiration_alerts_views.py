from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from vibestock.products.models import ExpirationAlert
from vibestock.products.serializers import ExpirationAlertSerializer


EXPIRATION_ALERT_URL = reverse('products:expiration-alerts-list')


def create_expiration_alert(
    user,
    number_of_days=8,
):
    return ExpirationAlert.objects.create(
        user=user,
        number_of_days=number_of_days
    )


class PublicExpirationAlertAPITests(TestCase):
    """ Test the publicly available expiration alerts API """

    def setUp(self):
        self.client = APIClient()

    def test_list_login_required(self):
        """ Test that login is required for retrieving expiration alerts """
        res = self.client.get(EXPIRATION_ALERT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_login_required(self):
        """ Test that login is required for retrieving products """
        res = self.client.post(EXPIRATION_ALERT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExpirationAlertAPITests(TestCase):
    """ Test the authorized user expiration alerts API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpassword',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        create_expiration_alert(self.user)
        create_expiration_alert(self.user, 13)

        res = self.client.get(EXPIRATION_ALERT_URL)

        expiration_alerts = ExpirationAlert.objects.all()
        serializer = ExpirationAlertSerializer(expiration_alerts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_only_user_products(self):
        """Test that products returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='test2@email.com',
            password='testpassword',
        )
        create_expiration_alert(user2, 13)

        expiration_alert = create_expiration_alert(self.user)

        res = self.client.get(EXPIRATION_ALERT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], str(expiration_alert.id))

    def test_product_create(self):
        payload = {
            'number_of_days': '8',
        }

        res = self.client.post(EXPIRATION_ALERT_URL, payload)

        expiration_alert = ExpirationAlert.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(payload['number_of_days']), expiration_alert.number_of_days)

    def test_product_delete(self):
        expiration_alert = create_expiration_alert(self.user)

        res = self.client.delete(reverse('products:expiration-alerts-detail', args=[expiration_alert.id]))

        expiration_alert_exists = ExpirationAlert.objects.filter(
            id=expiration_alert.id
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(expiration_alert_exists)
