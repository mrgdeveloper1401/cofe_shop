from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.template import models


class HeaderSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeaderSite
        fields = ("title",)


class SlideImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta : 
        model = models.SlideImage
        fields = ("image_url",)

    @extend_schema_field(serializers.URLField())
    def get_image_url(self, obj):
        return obj.image.get_image_url


class SlideBoxSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.SlideBox
        fields = ("title", "link", "image_url")

    @extend_schema_field(serializers.URLField())
    def get_image_url(self, obj):
        return obj.image.get_image_url


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
