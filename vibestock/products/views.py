from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from vibestock.products.models import Product, ExpirationAlert
from vibestock.products.serializers import ProductSerializer, ExpirationAlertSerializer
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


class ExpirationAlertCreateListDestroyViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):

    serializer_class = ExpirationAlertSerializer

    def get_queryset(self):
        return ExpirationAlert.objects.filter(
            user=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
