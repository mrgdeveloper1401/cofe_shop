from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by_id", "get_uploaded_by_username", "image_id_ba_salam", "created_at", "updated_at", "size", "width", "height", "is_active")
    raw_id_fields = ("created_by",)
    list_display_links = ("id", "created_by_id")
    list_per_page = 20
    list_filter = ("is_active", "created_at")
    search_fields = ("created_by__phone",)
    search_help_text = _("برای جست و جو  میتوانید از شماره  تلفن کاربر استفاده کنید")

    def get_uploaded_by_username(self, obj):
        return obj.created_by.phone
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("created_by").only(
            "created_by__phone",
            "image_id_ba_salam",
            "created_at",
            "updated_at",
            "size",
            "width",
            "height",
            "is_active"
        )
