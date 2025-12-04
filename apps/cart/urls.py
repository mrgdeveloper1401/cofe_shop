from django.urls import path
from apps.cart import api

urlpatterns = [
    path("product-cart/<product_id>/",api.ProductCartHandelerAPIView.as_view(),name="product-cart-handler"),
    path("delete-product-cart/<product_id>/",api.DeleteProductCartAPIView.as_view(),name="delete-product-cart"),
    path("detail/",api.CartDetailAPIView.as_view(),name="cart-detail"),
]