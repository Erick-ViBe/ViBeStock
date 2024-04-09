from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from datetime import date

from vibestock.products.models import Product
from vibestock.products.serializers import ProductSerializer


PRODUCTS_URL = reverse('products:product-list')


def product_detail_url(product_id):
    """ Return reversed product detail url """
    return reverse('products:product-detail', args=[product_id])

def create_product(
    user,
    name='Product name',
    description='Product description',
    stock=123,
    expiration_date=date(2024, 5, 5)
):
    return Product.objects.create(
        user=user,
        name=name,
        description=description,
        stock=stock,
        expiration_date=expiration_date,
    )


class PublicProductAPITests(TestCase):
    """ Test the publicly available products API """

    def setUp(self):
        self.client = APIClient()

    def test_list_login_required(self):
        """ Test that login is required for retrieving products """
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_login_required(self):
        """ Test that login is required for retrieving products """
        res = self.client.post(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductAPITests(TestCase):
    """ Test the authorized user products API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpassword',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        create_product(self.user)
        create_product(
            user=self.user,
            name='Product name 2',
            description='Product description 2',
            stock=321,
            expiration_date=date(2024, 6, 6)
        )

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('name')
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_only_user_products(self):
        """Test that products returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='test2@email.com',
            password='testpassword',
        )
        create_product(
            user=user2,
            name='Product name user 2',
            description='Product description user 2',
            stock=123,
            expiration_date=date(2024, 5, 5)
        )

        product = create_product(self.user)

        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], str(product.id))

    def test_retrieve_products_status_filter(self):
        expired_product = create_product(
            user=self.user,
            name='Product name',
            description='Product description',
            stock=123,
            expiration_date=date(2022, 5, 5)
        )
        usable_product = create_product(
            user=self.user,
            name='Product name 2',
            description='Product description 2',
            stock=321,
            expiration_date=date(2030, 6, 6)
        )

        res = self.client.get(
            PRODUCTS_URL,
            {'status': 'EXPIRED'}
        )

        expired_product_serializer = ProductSerializer(expired_product)
        usable_product_serializer = ProductSerializer(usable_product)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertIn(expired_product_serializer.data, res.data)
        self.assertNotIn(usable_product_serializer.data, res.data)

    def test_product_detail(self):
        product = create_product(self.user)

        url = product_detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductSerializer(product)

        self.assertEqual(res.data, serializer.data)

    def test_product_create(self):
        payload = {
            'name': 'string',
            'description': 'string',
            'stock': 32767,
            'expiration_date': '2024-04-17',
        }

        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        product = Product.objects.get(id=res.data['id'])

        self.assertEqual(payload['name'], product.name)
        self.assertEqual(payload['description'], product.description)
        self.assertEqual(payload['stock'], product.stock)
        self.assertEqual(payload['expiration_date'], product.expiration_date.strftime('%Y-%m-%d'))

    def test_product_partial_update(self):
        product = create_product(self.user)

        payload = {
            'name': 'Pruduct updated name'
        }

        url = product_detail_url(product.id)
        res = self.client.patch(url, payload)

        product.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(product.name, payload['name'])

    def test_product_full_update(self):
        product = create_product(self.user)

        payload = {
            'name': 'name updated',
            'description': 'description updated',
            'stock': 321,
            'expiration_date': '2024-05-05',
        }

        url = product_detail_url(product.id)
        self.client.put(url, payload)

        product.refresh_from_db()

        self.assertEqual(product.name, payload['name'])
        self.assertEqual(product.description, payload['description'])
        self.assertEqual(product.stock, payload['stock'])

    def test_product_delete(self):
        product = create_product(self.user)

        url = product_detail_url(product.id)
        self.client.delete(url)

        product_exists = Product.objects.filter(
            id=product.id
        ).exists()

        self.assertFalse(product_exists)
