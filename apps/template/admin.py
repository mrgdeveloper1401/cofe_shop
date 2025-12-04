from django.contrib import admin
from nested_inline.admin import NestedModelAdmin,NestedTabularInline
from apps.template.models import (
    SlideBox,
    SlideImage,
    SliderConfig,
    Footer,
    FooterLink,
    GrouLinkFooter,
    License
)

class SlideImageInline (admin.TabularInline) : 
    extra = 0
    exclude = ["id"]
    model = SlideImage


class SlideBoxInline (admin.TabularInline) : 
    extra = 0
    exclude = ['id']
    model = SlideBox

@admin.register(SliderConfig)
class SliderConfigAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    inlines = [SlideImageInline,SlideBoxInline]


class LicenseInline (NestedTabularInline) : 
    model = License
    extra = 0
    exclude = ["id"]


class FooterLinkInline (NestedTabularInline) : 
    model = FooterLink
    exclude = ["id"]
    extra = 0


class GrouLinkFooterInline (NestedTabularInline) : 
    model = GrouLinkFooter
    exclude = ["id"]
    extra = 0
    inlines = [FooterLinkInline]

@admin.register(Footer)
class FooterAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    list_display = ["is_active","phone","email","address"]

    inlines = [LicenseInline,GrouLinkFooterInline]

