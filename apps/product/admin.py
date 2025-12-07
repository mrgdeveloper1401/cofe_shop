from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from apps.product import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 0
    raw_id_fields = ("image",)


class ProductFeatureInline(admin.TabularInline):
    model = models.ProductFeature
    extra = 0
    raw_id_fields = ("key",)


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


# @admin.register(Country)
# class CountryAdmin (admin.ModelAdmin):
#     list_display_links = ("id", "name")
#     raw_id_fields = ("flag",)
#     list_per_page = 20
#     list_filter = ("is_active", )
#     search_fields = ("name",)
#     search_help_text = _("برای جست و جو میتوانید از نام کشور استفاده کنید")
#     list_display = ("id", "name", "flag_id", "is_active", "created_at", "updated_at", "is_active")
#     list_editable = ("is_active",)


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    raw_id_fields = ("logo",)
    list_display = ("id", "is_own", "logo_id", "name", "created_at", "is_active")
    list_display_links = ("id", "is_own")
    search_fields = ("name",)
    search_help_text = _("برای جست و جو میتوانید از نام برند استفاده کنید")
    list_per_page = 20
    list_filter = ("is_active", )
    list_editable = ("is_active",)


@admin.register(models.Product)
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


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ("category_image", "parent")
    list_display = ("id", "title", "category_image_id", "parent_id", "is_active", "created_at", "updated_at")
    list_per_page = 20
    list_editable = ("is_active",)
    list_filter = ("is_active", ParentCategoryFilter)
    list_display_links = ("id", "title")
    search_fields = ("title",)
    search_help_text = _("برای جست و جو میتوانید از نام دسته بندی استفاده کنید")


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    raw_id_fields = ("product", "image")
    list_display = ("id", "product_id", "image_id", "created_at", "updated_at", "is_active")
    list_filter = ("is_active",)
    list_per_page = 20
    list_editable = ("is_active",)
    list_display_links = ("id", "product_id", "image_id")


@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "product_id", "parent_id", "rating", "is_active", "created_at", "updated_at")
    list_per_page = 20
    list_filter = ("is_active", "created_at", ParentCategoryFilter)
    search_fields = ("user__phone", "user__username")
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل یا یوزرنیم کاربر استفاده کنید")
    raw_id_fields = ('product', "user")
    list_editable = ("is_active",)


@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    list_per_page = 20
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    list_display_links = ("id", 'name')


@admin.register(models.ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display_links = ("id", "product_id")
    raw_id_fields = ("product", "key")
    list_display = ("id", "product_id", "key_name", "value", "created_at", "updated_at", 'is_active')
    list_editable = ("is_active",)
    list_filter = ("is_active", "created_at")
    list_per_page = 20
    search_fields = ("key__name",)
    search_help_text = _("برای جست و جو میتوانید از عنوان کلید استفاده کنید")

    def key_name(self, obj):
        return obj.key.name

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("key").only(
            "product_id",
            "key__name",
            "value",
            "is_active",
            "created_at",
            "updated_at"
        )
