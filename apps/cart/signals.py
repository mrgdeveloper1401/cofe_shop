from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from apps.cart.models import CartProduct,Cart


@receiver(signal=post_delete,sender=CartProduct)
@receiver(signal=post_save,sender=CartProduct)
def calucale_total_price (sender,instance : CartProduct,**kwargs) : 
    if instance.cart : 
        total_price = 0
        for cart_product in instance.cart.cart_products.all() : 
            total_price += cart_product.product.price * cart_product.count
        cart = Cart.objects.filter(id=instance.cart.id).first()
        if cart : 
            cart.total_price = total_price 
            cart.save(update_fields=["total_price"])