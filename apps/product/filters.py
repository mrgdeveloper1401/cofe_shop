from django_filters import rest_framework as filters
from apps.product import models


class ProductFilters(filters.FilterSet):
    has_discount = filters.BooleanFilter(method='filter_has_discount', field_name='discount_percent')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = models.Product
        fields = {
            "is_available": ("exact",)
        }

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(
                discount_percent__gt=0
            )
        return queryset
