from rest_framework import serializers

from apps.product.serializers import BrandSerializer,CountrySerializer,ProductCategorySerializer
from apps.template import models


class HeaderSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeaderSite
        fields = ("title",)


class SlideImageSerializer(serializers.ModelSerializer):
    class Meta : 
        model = models.SlideImage
        exclude = ["id","slider"]


class SlideBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlideBox
        fields = "__all__"


class SliderConfigSerializer (serializers.ModelSerializer) : 

    boxes = SlideBoxSerializer(many=True)

    images = SlideImageSerializer(many=True)

    class Meta : 
        model = models.SliderConfig
        exclude = ["id"]


class LicenseSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = models.License
        exclude = ["id","footer"]

class FooterLinkSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = models.FooterLink
        exclude = ["id","group_link"]

class GrouLinkFooterSerializer (serializers.ModelSerializer) : 

    links = FooterLinkSerializer(many=True)

    class Meta : 
        model = models.GrouLinkFooter
        exclude = ["id","footer"]

class FooterSerializer (serializers.ModelSerializer) :

    licenses = LicenseSerializer(many=True) 

    group_links = GrouLinkFooterSerializer(many=True)
    
    class Meta : 
        model = models.Footer
        exclude = ["id","is_active"]


class LayoutSerializer (serializers.Serializer) : 

    footer = FooterSerializer()

class IndexSerializer (serializers.Serializer) : 

    car_brands = BrandSerializer(many=True)

    brand_countries = CountrySerializer(many=True)

    yadak_sadra_brands = BrandSerializer(many=True)

    slider = SliderConfigSerializer()

    product_categoris = ProductCategorySerializer(many=True)