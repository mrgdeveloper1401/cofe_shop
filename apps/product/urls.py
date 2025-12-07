from django.urls import path
from rest_framework_nested import routers
from apps.product import views


app_name = "v1_product"

router = routers.SimpleRouter()
router.register("products", views.ProductView, basename="products")

product_router = routers.NestedSimpleRouter(router, "products", lookup='product')
product_router.register("product_comment", views.ProductReviewView, basename="product_review")

urlpatterns = [
    path("parent_category/", views.ParentProductCategoryView.as_view(), name='parent_category'),
] + router.urls + product_router.urls
