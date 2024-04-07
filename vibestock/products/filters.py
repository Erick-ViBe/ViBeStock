from django_filters import FilterSet, DateFilter

from vibestock.products.models import Product


class ProductFilter(FilterSet):
    expiration_start_date = DateFilter(field_name='expiration_date', lookup_expr="gte")
    expiration_end_date = DateFilter(field_name='expiration_date', lookup_expr="lte")

    class Meta:
        model = Product
        fields = [
            'expiration_start_date',
            'expiration_end_date',
            'status',
        ]
