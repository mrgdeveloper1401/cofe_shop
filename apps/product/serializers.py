from rest_framework import serializers
from apps.product import models


class ParentProductCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductCategory
        fields = ("id", "title", "image_url")
        
    def get_image_url(self, obj):
        return obj.category_image.get_image_url


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductImage
        fields = (
            "image_url",
        )

    def get_image_url(self, obj):
        return obj.image.get_image_url


class ProductSerializet(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = (
            "id",
            "category_id",
            "title",
            "slug",
            "price",
            "discount_percent",
            "short_description",
            "is_available",
            "stock",
            "meta_title",
            "meta_description",
            "created_at",
            "updated_at",
            "images"
        )


class ProductFetureSerializer(serializers.ModelSerializer):
    key_name = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductFeature
        fields = (
            "key_name",
            "value"
        )

    def get_key_name(self, obj):
        return obj.key.name


class RetrieveProductSerializer(ProductSerializet):
    product_features = ProductFetureSerializer(many=True)

    class Meta(ProductSerializet.Meta):
        model = models.Product
        fields = ProductSerializet.Meta.fields + ("short_description", "description", "product_features")
