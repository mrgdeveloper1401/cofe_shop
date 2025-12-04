from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from django.db.models import Count
from apps.product.models import Brand,Country,ProductCategory
from apps.product.serializers import (
    BrandSerializer,
    CountrySerializer,
    ProductCategorySerializer
)
from apps.template.serializers import (
    IndexSerializer,
    SliderConfigSerializer,
    FooterSerializer,
    LayoutSerializer
)
from apps.template.models import SliderConfig,Footer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IndexAPIView(APIView) : 


    @swagger_auto_schema(
        operation_summary="Index Page",
        responses={
            200 : openapi.Response("Ok",IndexSerializer())
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
            "slider" : SliderConfigSerializer(
                SliderConfig.objects.filter(is_active=True).last(),
                context={"request" : request},
            ).data,
            "product_categories" : ProductCategorySerializer(
                ProductCategory.objects.all()[0:5],
                many=True,
                context={'request' : request}
            ).data,
        }
        return Response(data=data,status=status.HTTP_200_OK)
    




class LayoutAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="Header And Footer",
        responses={
            200 : LayoutSerializer(),
        }
    )
    def get (self,request) : 
        data = {
            "footer" : FooterSerializer(
                Footer.objects.filter(is_active=True).last(),
                context={"request":request},
            ).data,
        }
        return Response(data,status.HTTP_200_OK)