from django.db.models import Prefetch
from rest_framework import views, response, mixins, viewsets, filters
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from apps.product import models
from apps.product import serializers
from apps.product.filters import ProductFilters


class ParentProductCategoryView(views.APIView):
    serializer_class = serializers.ParentProductCategorySerializer

    def get(self, request):
        get_cache = cache.get("parent_category")
        if get_cache:
            return response.Response(get_cache)
        
        quryset = models.ProductCategory.objects.filter(
            is_active=True,
            ).select_related("category_image").only(
                "title",
                "category_image__image"
            )
        serializer = self.serializer_class(quryset, many=True)
        
        # set cache
        cache.set("parent_category", serializer.data, timeout=60 * 60 * 24 * 30)
        
        # respone data
        return response.Response(serializer.data)


class ProductView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    filterset_class = ProductFilters
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at",)

    def get_queryset(self):
        base_query = models.Product.objects.filter(
            is_active=True
        ).prefetch_related(
            Prefetch(
                "images", models.ProductImage.objects.filter(is_active=True).select_related("image").only("image__image", "product_id")
            )
        )

        base_fields = ('category_id', 'title', 'slug', 'price', 'discount_percent', 'short_description', 'is_available', 'stock', 'meta_title', 'meta_description', 'created_at', 'updated_at')
        retrieve_fields = base_fields + ("short_description", "description")

        if self.action == "list":
            return base_query.only(*base_fields)
        else:
            return base_query.only(*retrieve_fields).prefetch_related(
                Prefetch(
                    "product_features", models.ProductFeature.objects.filter(is_active=True).select_related("key").only("product_id", "key__name", "value")
                )
            )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.RetrieveProductSerializer
        else:
            return serializers.ProductSerializet
