from django.urls import path, include

from rest_framework.routers import DefaultRouter

from vibestock.products.views import ProductViewSet, ExpirationAlertsCreateListDestroyViewSet


router = DefaultRouter()
router.register(r'products/expiration_alerts', ExpirationAlertsCreateListDestroyViewSet, basename='expiration-alerts')
router.register(r'products', ProductViewSet, basename='product')

app_name = 'products'


urlpatterns = [
    path(
        '',
        include(router.urls)
    )
]
