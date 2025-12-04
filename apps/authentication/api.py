from datetime import timedelta
import random
import hashlib
import time
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import constant_time_compare
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.serializers import (
    RegisterSerializer,
    UserSerializer,
    password_regex,
    LoginResponseSerializer,
)
from core.settings import SIMPLE_JWT
from apps.authentication.tasks import send_otp
from core.utils.jwt import get_tokens_for_user
from core.utils.permissions import NotAuthenticate



class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (NotAuthenticate,)

    @swagger_auto_schema(
        operation_summary="Register User",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username" : openapi.Schema(type=openapi.TYPE_STRING),
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
                "password" : openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=("username","phone","password"),
        ),
    )
    def post (self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # send otp by celery
        # send_otp.apply_async(
        #     args=[user.id],
        #     link=check_user_is_active.si(user.id)
        # )

        # create token
        token = get_tokens_for_user(user)
        data = {
            "token": token,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "expired_date": timezone.now() + timedelta(days=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days),
            "expire_timestamp": time.time() + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class ActivateUserAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="Activate User Account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
                "otp_code" : openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["phone","otp_code"],
        ),
        responses={
            "200" : LoginResponseSerializer(),
        }
    )
    def post (self,request) : 
        try : 
            phone = request.data["phone"]
        except : 
            return Response({"phone" : "required ."},status.HTTP_400_BAD_REQUEST)

        try : 
            otp_code = request.data["otp_code"]
        except : 
            return Response({"otp_code" : "required ."},status.HTTP_400_BAD_REQUEST)
        
        # get user 
        try : 
            user = get_user_model().objects.get(phone=phone)
        except get_user_model().DoesNotExist : 
            return Response({"error" : "user does not exist ."},status.HTTP_400_BAD_REQUEST)
        
        # change otp code to hashed
        hashed_otp = hashlib.sha256(str(otp_code).encode("utf-8"))
        if constant_time_compare(hashed_otp.hexdigest(),user.opt_code_hashed) : 
            user.is_active = True
            user.change_otp_code(random.randint(9999,99999))
            refresh_token = RefreshToken().for_user(user)
            data = {
                "access_token" : str(refresh_token.access_token),
                "refresh_token" : str(refresh_token),
                "user" : UserSerializer(user).data,
            }
            return Response(data,status.HTTP_200_OK)
        else : 
            return Response({"error" : "invalid otp_code ."},status.HTTP_400_BAD_REQUEST)
        

class ChangeUserPassword (APIView) :

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="change password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password" : openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=["password"],
        )
    )
    def post (self,request) : 
        
        try : 
            password = request.data["password"]
        except : 
            return Response({"password" : "required ."},status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if password_regex.match(password) : 
            user.set_password(password)
            user.save()
            return Response({"data" : "password has beed changed ."},status.HTTP_200_OK)
        else : 
            return Response(
                {"password" : "password must contain upper,lower and interger character ."},
                status.HTTP_400_BAD_REQUEST
            )
        

class LoginAPIView (APIView) : 


    @swagger_auto_schema(
        operation_summary="login with password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
                "password" : openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=["phone","password"]
        ),
        responses={
            200 : LoginResponseSerializer(),
        }
    )
    def post (self,request) : 
        try : 
            phone = request.data["phone"]
        except : 
            return Response({"phone" : "required ."},status.HTTP_400_BAD_REQUEST)
        try : 
            password = request.data["password"]
        except : 
            return Response({"password" : "required ."},status.HTTP_400_BAD_REQUEST)
        
        try : 
            user = get_user_model().objects.get(phone=phone)
        except get_user_model().DoesNotExist : 
            return Response({"error" : "user does not exist ."},status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(password) : 
            refresh_token = RefreshToken().for_user(user)
            data = {
                "user" : UserSerializer(user).data,
                "access_token" : str(refresh_token.access_token),
                "refresh_token" : str(refresh_token),
            }
            return Response(data,status.HTTP_200_OK)
        else :
            return Response({"password" : "password is incorrect ."},status.HTTP_400_BAD_REQUEST)
    

class SendOptCodeAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="Send Otp Code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["phone"],
        )
    )
    def post (self,request) : 
        try : 
            phone = request.data.get("phone")
        except : 
            return Response({"error": "phone is required ."},status=status.HTTP_400_BAD_REQUEST)
        
        try : 
            user = get_user_model().objects.get(phone=phone)
        except get_user_model().DoesNotExist : 
            return Response({"error" : "user does not exist ."},status.HTTP_400_BAD_REQUEST)
        
        send_otp.apply_async(args=[user.id])
        return Response({"data": "opt has been sent ."},status.HTTP_200_OK)