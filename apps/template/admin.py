from django.contrib import admin
from django.http.response import Header
from nested_inline.admin import NestedModelAdmin, NestedTabularInline
from django.utils.translation import gettext_lazy as _

from apps.template.models import (
    HeaderSite,
    SlideBox,
    SlideImage,
    SliderConfig,
    Footer,
    FooterLink,
    GrouLinkFooter,
    License
)

class SlideImageInline(admin.TabularInline):
    extra = 0
    model = SlideImage


class SlideBoxInline(admin.TabularInline):
    extra = 0
    model = SlideBox


class LicenseInline(NestedTabularInline):
    model = License
    extra = 0


class FooterLinkInline(NestedTabularInline):
    model = FooterLink
    extra = 0


class GrouLinkFooterInline(NestedTabularInline):
    model = GrouLinkFooter
    extra = 0
    inlines = (FooterLinkInline,)


@admin.register(Footer)
class FooterAdmin(NestedModelAdmin):
    list_display = ("id", "phone","is_active","email","address")
    list_display_links = ("id", "phone")
    inlines = (LicenseInline, GrouLinkFooterInline)


@admin.register(SliderConfig)
class SliderConfigAdmin(admin.ModelAdmin):
    inlines = (SlideImageInline, SlideBoxInline)


@admin.register(SlideBox)
class SlideBoxAdmin(admin.ModelAdmin):
    list_display = ("id", "image_id", "title", "is_active", "created_at", "updated_at")
    list_display_links = ("id", "image_id", "title")
    list_per_page = 20
    list_editable = ("is_active",)
    search_fields = ("title",)
    search_help_text = _("برای جست و جو میتوانید از عنوان استفاده کنید")
    raw_id_fields = ("image", "slider")
    list_filter = ("is_active", "created_at")


@admin.register(SlideImage)
class SlideImageAdmin(admin.ModelAdmin):
    raw_id_fields = ("slider", "image")
    list_display = ("id", "slider_id", "image_id", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    list_display_links = ("id", "slider_id", "image_id")
    list_per_page = 20
    list_editable = ("is_active",)


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(GrouLinkFooter)
class GrouLinkFooterAdmin(admin.ModelAdmin):
    pass


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(HeaderSite)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    list_display_links = ("id", "title")
    list_per_page = 20
    search_fields = ("title",)
    search_help_text = _("برای جست و جو میتوانید از عنوان هدر استفاده کنید")
    list_editable = ("is_active",)
