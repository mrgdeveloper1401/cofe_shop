from django.contrib import admin
from apps.cart.models import Cart,CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    pass
