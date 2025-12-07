from django.core.cache import cache
from rest_framework import views, response
from rest_framework import status


from apps.product.models import Brand,Country,ProductCategory
from apps.product.serializers import (
    BrandSerializer,
    CountrySerializer,
    ProductCategorySerializer
)
from apps.template import serializers
from apps.template import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HeaderSiteView(views.APIView):
    serializer_class = serializers.HeaderSiteSerializer

    def get(self, request):
        # get cache
        get_value =cache.get("header_site")
        if get_value:
            return response.Response(get_value)

        # query and serializer data
        queryset = models.HeaderSite.objects.filter(is_active=True).only("title")
        serializer = self.serializer_class(queryset, many=True)

        # set cache
        cache.set("header_site", serializer.data, timeout=60 * 60 * 24 * 30)

        # response data
        return response.Response(serializer.data)


class SliderBoxView(views.APIView):
    serializer_class = serializers.SlideBoxSerializer

    def get(self, request):
        # get cache 
        get_value = cache.get("slider_box")
        if get_value:
            return response.Response(get_value)

        queryset = models.SlideBox.objects.filter(is_active=True).select_related("image").only(
            "title",
            "link",
            "image__image"
        )
        serializer = self.serializer_class(queryset, many=True)
        
        # set cache
        cache.set("slider_box", serializer.data, timeout=60 * 60 * 24 * 30)
        
        # response data
        return response.Response(serializer.data)


class IndexAPIView(views.APIView) : 


    @swagger_auto_schema(
        operation_summary="Index Page",
        responses={
            200 : openapi.Response("Ok",serializers.IndexSerializer())
        }
    )
    def get(self,request) : 

        print(ProductCategory.objects.all())

        data = {
            "car_brands" : BrandSerializer(
                Brand.objects.filter(is_own=False),
                many=True,
                context={"request":request}).data,
            "brand_countries" : CountrySerializer(
                Country().get_most_brands(),
                many=True,
                context={'request': request}
            ).data,
            "yadak_sadra_brands" : BrandSerializer(
                Brand.objects.filter(is_own=True)[:6],
                many=True,
                context={"request":request}).data,
            "slider" : serializers.SliderConfigSerializer(
                models.SliderConfig.objects.filter(is_active=True).last(),
                context={"request" : request},
            ).data,
            "product_categories" : ProductCategorySerializer(
                ProductCategory.objects.all()[0:5],
                many=True,
                context={'request' : request}
            ).data,
        }
        return response.Response(data=data,status=status.HTTP_200_OK)
    




class LayoutAPIView (views.APIView) : 

    @swagger_auto_schema(
        operation_summary="Header And Footer",
        responses={
            200 : serializers.LayoutSerializer(),
        }
    )
    def get (self,request) : 
        data = {
            "footer" : serializers.FooterSerializer(
                models.Footer.objects.filter(is_active=True).last(),
                context={"request":request},
            ).data,
        }
        return response.Response(data,status.HTTP_200_OK)