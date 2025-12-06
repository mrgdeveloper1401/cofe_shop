from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.product.models import (
    Brand,
    Country,
    Product,
    ProductImage,
    ProductCategory,
    ProductFeature,
    ProductReview
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    raw_id_fields = ("logo",)
    list_display = ("id", "is_own", "logo_id", "name", "created_at", "is_active")
    list_display_links = ("id", "is_own")
    search_fields = ("name",)
    search_help_text = _("برای جست و جو میتوانید از نام برند استفاده کنید")
    list_per_page = 20
    list_filter = ("is_active", )
    list_editable = ("is_active",)


@admin.register(Country)
class CountryAdmin (admin.ModelAdmin):
    list_display_links = ("id", "name")
    raw_id_fields = ("flag",)
    list_per_page = 20
    list_filter = ("is_active", )
    search_fields = ("name",)
    search_help_text = _("برای جست و جو میتوانید از نام کشور استفاده کنید")
    list_display = ("id", "name", "flag_id", "is_active", "created_at", "updated_at", "is_active")
    list_editable = ("is_active",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    exclude = ("id",)


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0
    exclude = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, ProductFeatureInline)
    list_display_links = ("id", "title")
    raw_id_fields = ("category", "brand")
    prepopulated_fields = {
        "slug": ("title",)
    }
    filter_horizontal = ("similar_products",)
    list_display = ("id", "title", "price", "discount_percent", "is_available", "is_active", "stock", "created_at")
    list_per_page = 20
    list_editable = ("price", "discount_percent", "is_available", "is_active", "stock")
    list_filter = ("is_active", "is_available")
    search_fields = ("title",)
    search_help_text = _("برای جست و جو میتوانید از عنوان دسته بندی استفاده کنید")


class ParentCategoryFilter(admin.SimpleListFilter):
    title = _("check parent")
    parameter_name = "parent"

    def lookups(self, request, model_admin):
        look = (
            ("have_parent", _("have parent")),
            ("no_parent", _("no parent"))
        )
        return look
    
    def queryset(self, request, queryset):
        if self.value() == "have_parent":
            return queryset.filter(
                parent__isnull=False
            )
        if self.value() == "no_parent":
            return queryset.filter(
                parent__isnull=True
            )


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ("category_image", "parent")
    list_display = ("id", "title", "category_image_id", "parent_id", "is_active", "created_at", "updated_at")
    list_per_page = 20
    list_editable = ("is_active",)
    list_filter = ("is_active", ParentCategoryFilter)
    list_display_links = ("id", "title")
    search_fields = ("title",)
    search_help_text = _("برای جست و جو میتوانید از نام دسته بندی استفاده کنید")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    raw_id_fields = ("product", "image")
    list_display = ("id", "product_id", "image_id", "created_at", "updated_at", "is_active")
    list_filter = ("is_active",)
    list_per_page = 20
    list_editable = ("is_active",)
    list_display_links = ("id", "product_id", "image_id")


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "product_id", "rating", "is_active", "created_at", "updated_at")
    list_per_page = 20
    list_filter = ("is_active", "created_at")
    search_fields = ("user__phone", "user__username")
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل یا یوزرنیم کاربر استفاده کنید")
    raw_id_fields = ('product', "user")
