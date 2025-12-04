from django.db import models
from django_uuid7 import UUID7Field
from django.contrib.auth import get_user_model
from apps.core_app.models import ActiveMixin, CreateMixin, UpdateMixin
from apps.product.models import Product


class Cart(ActiveMixin, UpdateMixin, CreateMixin):
    id = UUID7Field(primary_key=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        related_name="carts",
    )
    is_open = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart"


class CartProduct(ActiveMixin, UpdateMixin, CreateMixin):
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.PROTECT,
        related_name="cart_products"
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "cart_product"
