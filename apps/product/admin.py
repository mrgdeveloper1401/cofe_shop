from django.contrib import admin
from apps.product.models import (
    Brand,
    Country,
    Product,
    ProductImage,
    ProductCategory,
    ProductFeature
)


@admin.register(Brand)
class BrandAdmin (admin.ModelAdmin) : 
    exclude = ("id","slug")


@admin.register(Country)
class CountryAdmin (admin.ModelAdmin) : 
    exclude = ("id","slug")


class ProductImageInline (admin.TabularInline) : 
    model = ProductImage
    extra = 0
    exclude = ("id",)


class ProductFeatureInline (admin.TabularInline) : 
    model = ProductFeature
    extra = 0
    exclude = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline,ProductFeatureInline,)
    raw_id_fields = ("category",)
    prepopulated_fields = {
        "slug": ("title",)
    }


@admin.register(ProductCategory)
class ProductCategoryAdmin (admin.ModelAdmin) : 
    raw_id_fields = ("category_image", "parent")