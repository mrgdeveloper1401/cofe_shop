from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


class ProductReviewSerializer(serializers.ModelSerializer):
    parent_number = serializers.IntegerField(required=False)
    username = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductReview
        fields = (
            "id",
            "rating",
            "comment",
            "parent_id",
            "parent_number",
            "lft",
            "rght",
            "level",
            "tree_id",
            "username",
            "is_owner"
        )
        extra_kwargs = {
            "lft": {"read_only": True},
            "rght": {"read_only": True},
            "level": {"read_only": True},
            "tree_id": {'read_only': True},
            "parent_id": {"read_only": True}
        }

    def create(self, validated_data):
        parent_number = validated_data.pop("parent_number", None)
        user_id = self.context['request'].user.id
        product_id = int(self.context['product_pk'])

        if parent_number is None:
            return models.ProductReview.objects.create(user_id=user_id, product_id=product_id, **validated_data)
        else:
            parent_obj = get_object_or_404(models.ProductReview, is_active=True, id=parent_number, product_id=product_id)
            return models.ProductReview.objects.create(user_id=user_id, product_id=product_id, parent_id=parent_obj.id, **validated_data)

    @extend_schema_field(serializers.CharField())
    def get_username(self, obj):
        return obj.user.username

    @extend_schema_field(serializers.CharField())
    def get_is_owner(self, obj):
        user_id = self.context['request'].user.id
        return obj.user_id == user_id
