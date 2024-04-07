from django.urls import path, include

from rest_framework.routers import DefaultRouter

from vibestock.products.views import ProductViewSet


router = DefaultRouter()
router.register('', ProductViewSet, basename='Product')

app_name = 'products'


urlpatterns = [
    path(
        '',
        include(router.urls)
    )
]
