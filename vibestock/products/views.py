from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from vibestock.products.models import Product
from vibestock.products.serializers import ProductSerializer
from vibestock.products.filters import ProductFilter


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name', 'stock', 'expiration_date']
    ordering = ['name']
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
