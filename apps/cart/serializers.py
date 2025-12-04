from rest_framework import serializers
from apps.cart.models import Cart,CartProduct
from apps.product.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta : 
        model = CartProduct
        exclude = ("id","cart")


class CartSerializer(serializers.ModelSerializer):
    cart_products = serializers.SerializerMethodField()

    def get_cart_products (self, obj) : 
        objects = obj.cart_products.all().order_by("id")
        return CartProductSerializer(objects, many=True, context=self.context).data

    class Meta : 
        model = Cart
        exclude = ("id","user")

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["date"] = instance.date.strftime("%Y-%m-%d")
        context["time"] = instance.date.strftime("%H:%M:%S")
        return context
