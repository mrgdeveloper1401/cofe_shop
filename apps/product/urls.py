from django.urls import path
from rest_framework import routers
from apps.product import views


app_name = "v1_product"

router = routers.SimpleRouter()
router.register("products", views.ProductView, basename="products")

urlpatterns = [
    path("parent_category/", views.ParentProductCategoryView.as_view(), name='parent_category'),
] + router.urls
