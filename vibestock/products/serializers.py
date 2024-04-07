from rest_framework import serializers

from vibestock.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'expiration_date']
