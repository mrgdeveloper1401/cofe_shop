from django.urls import path
from apps.product import api

urlpatterns = [

    path("category/<slug>/",api.ProductCategoryAPIView.as_view(),name="product-category"),

    path("search/",api.ProductSearchAPIView.as_view(),name="product-search"),

    path("<slug>/",api.ProductDetailAPIView.as_view(),name="product-detail"),
]