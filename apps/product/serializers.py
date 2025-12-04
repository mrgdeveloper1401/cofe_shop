from rest_framework import serializers
from apps.product.models import (
    Brand,Country,Product,ProductCategory,ProductImage,
    ProductFeature
)


class ProductCategorySerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProductCategory
        exclude = ["id"]

class CountrySerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Country
        exclude = ["id"]

class BrandSerializer (serializers.ModelSerializer) : 

    country = CountrySerializer()

    class Meta : 
        model = Brand
        exclude = ["id"]


class ProductSerializer (serializers.ModelSerializer) : 

    category = ProductCategorySerializer()

    country = CountrySerializer()

    brand = BrandSerializer()

    class Meta : 
        model = Product
        fields = ["id","slug","title","main_image","price","country","category","brand"]
    

class ProductImageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProductImage
        fields = ["image"]


class ProductFeatureSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProductFeature
        fields = ["key","value"]

class ProductDetailSerializer (serializers.ModelSerializer) : 
    
    category = ProductCategorySerializer()

    country = CountrySerializer()

    brand = BrandSerializer()

    images = ProductImageSerializer(many=True)

    product_features = ProductFeatureSerializer(many=True)

    similar_products = ProductSerializer(many=True)

    class Meta : 
        model = Product
        fields = "__all__"

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["time_added"] = instance.time_added.strftime("%Y-%M-%d")
        return context



class ProductCategoryResponseSerializer (serializers.Serializer) : 

    products = ProductSerializer(many=True)

    count = serializers.IntegerField()