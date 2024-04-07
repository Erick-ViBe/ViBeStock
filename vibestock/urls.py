from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = 'ViBeStock',
        default_version = 'v1',
        description = 'Inventory management and expiration dates',
        contact = openapi.Contact(
            name = 'Erick ViBe',
            url = 'https://erickvibe.xyz/',
            email = 'sergio.erick.vicencio.benitez@gmail.com',
        ),
        license = openapi.License(name = 'BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/', include('vibestock.users.urls')),
    path('api/products/', include('vibestock.products.urls')),
]
