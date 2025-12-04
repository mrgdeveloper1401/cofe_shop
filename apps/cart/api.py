from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.product.models import Product
from apps.cart.models import Cart,CartProduct
from apps.cart.serializers import CartSerializer
from drf_yasg.utils import swagger_auto_schema


class ProductCartHandelerAPIView (APIView) : 

    permission_classes = [IsAuthenticated]
    
    def get_objects (self,request,product_id) : 
        try : 
            self.product = Product.objects.get(id=product_id)
        except : 
            return Response({"error" : "product with this id does not exist"},status.HTTP_404_NOT_FOUND) 
        
        self.cart,created = Cart.objects.get_or_create(user=request.user,is_open=True,is_paid=False)
        self.cart_product,created = CartProduct.objects.get_or_create(
            cart=self.cart,
            product=self.product
        )

    @swagger_auto_schema(
        operation_summary="Add Product To Cart"
    )
    def post (self,request,product_id) : 
        result = self.get_objects(request,product_id)
        if result : return result
        self.cart_product.count = self.cart_product.count + 1
        self.cart_product.save()
        return Response({"data" : "product is been added sucessfully"},status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Remove One By One From The Cart"
    )
    def delete (self,request,product_id) : 
        result = self.get_objects(request,product_id)
        if result : return result
        if self.cart_product.count in [0,1] : 
            self.cart_product.delete()
        else : 
            self.cart_product.count = self.cart_product.count - 1
            self.cart_product.save()
        return Response({"data" : "product has been decreased sucessfully"},status.HTTP_200_OK)
    

class DeleteProductCartAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete Product From Cart"
    )
    def delete (self,request,product_id) : 

        try : 
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist : 
            return Response({"error" : "product does not exist"},status.HTTP_404_NOT_FOUND)
        try : 
            active_cart = Cart.objects.get(user=request.user,is_open=True,is_paid=False)
        except : 
            return Response({"error" : "user hasnt got any active cart"},status.HTTP_400_BAD_REQUEST)
        product_cart = active_cart.cart_products.filter(product_id=product_id)
        print(product_cart)
        if product_cart : 
            product_cart.delete()
        return Response({"data": "product has been deleted"},status.HTTP_204_NO_CONTENT)
    

class CartDetailAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Cart Detail",
        responses={
            "200" : CartSerializer()
        }
    )
    def get (self,request) : 
        cart,_ = Cart.objects.get_or_create(
            user=request.user,
            is_open=True,
            is_paid=False
        )
        data = CartSerializer(cart,context={'request' : request}).data
        return Response(data,status.HTTP_200_OK)