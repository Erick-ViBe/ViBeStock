from django.contrib import admin

from vibestock.products.models import Product, ExpirationAlert


admin.site.register(Product)
admin.site.register(ExpirationAlert)
