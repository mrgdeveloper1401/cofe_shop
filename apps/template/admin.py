from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedTabularInline
from apps.template.models import (
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
    pass


@admin.register(SlideImage)
class SlideImageAdmin(admin.ModelAdmin):
    pass


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(GrouLinkFooter)
class GrouLinkFooterAdmin(admin.ModelAdmin):
    pass


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    pass
