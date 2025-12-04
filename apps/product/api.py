from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank
from apps.product.models import ProductCategory,Brand,Country,Product
from apps.product.serializers import (
    ProductSerializer,ProductCategoryResponseSerializer,
    BrandSerializer,CountrySerializer,ProductDetailSerializer
)
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count
from apps.product.tasks import calculate_similar_products
    



class ProductCategoryAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="Get Product Base on Category",
        responses={
            "200" : ProductCategoryResponseSerializer(),
        }
    )
    def get(self,request,slug) : 

        params = request.GET

        try : 
            products = ProductCategory.objects.get(slug=slug).products.select_related(
                "category","brand","country"
            ).only("id","slug","title","main_image","price","country","category","brand").all()
        except : 
            return Response(
                data={"error" : "not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if "brand" in params.keys() and params["brand"].strip() != "" : 
            brand = params["brand"].strip()
            products = products.filter(brand__slug=brand)
        
        if "country" in params.keys() and params["country"].strip() != "" : 
            country = params["country"]
            products = products.filter(country__slug=country)
        
        if "order" in params.keys() : 
            order = params["order"]
            match order : 
                case "new" : 
                    products = products.order_by("-time_added")
                case "expense" : 
                    products = products.order_by("-price")
                case "cheep" : 
                    products = products.order_by("price")

        data = {
            "products" : ProductSerializer(
                products,
                many=True,
                context={"request" : request},
            ).data,
            "count" : products.count(),
            "brands" : BrandSerializer(
                Brand.objects.annotate(product_count=Count("products")).order_by("-product_count")[0:5],
                many=True,
                context={"request" : request},
            ).data,
            "countries" : CountrySerializer(
                Country.objects.annotate(product_count=Count("products")).order_by("-product_count")[0:5],
                many=True,
                context={'request' : request}
            ).data,
        }
        return Response(data,status.HTTP_200_OK)
    


class ProductSearchAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="Search Product",
        operation_description="?search=....",
        responses={
            200 : ProductSerializer(many=True),
        }
    )
    def get (self,request : HttpRequest) : 
        search_param = request.query_params.get("search")
        objects = []
        if search_param : 
            vector = SearchVector("title","short_description")
            search_query = SearchQuery(search_param)
            objects = Product.objects.annotate(
                search=vector,
                rank=SearchRank(vector,search_query)
            ).select_related("category","brand","country").only(
                "id","slug","title","main_image","price","country","category","brand"
            ).filter(search=search_query).order_by("-rank")[0:6]
        data = ProductSerializer(
            objects,
            many=True,
            context={"request" : request}
        ).data
        return Response(data,status.HTTP_200_OK)
    


class ProductDetailAPIView (APIView) :  

    @swagger_auto_schema(
        operation_summary="Get Product Detail",
        responses={
            "200" : ProductDetailSerializer(),
        },
    )
    def get (self,request,slug) : 
        try : 
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist :
            return Response({"error": "product does not exist"},status.HTTP_200_OK)
        data = ProductDetailSerializer(product,context={"request" : request}).data
        return Response(data) 



