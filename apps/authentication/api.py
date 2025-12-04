from datetime import timedelta
import random
import hashlib
import time
from django.utils import timezone
from rest_framework.exceptions import NotFound
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
    ChangePasswordSerializer,
    LoginResponseSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    password_regex
)
from core.settings import SIMPLE_JWT
from apps.authentication.tasks import send_otp
from core.utils.exceptions import PasswordNotEqaul, PasswordNotMatch
from core.utils.jwt import get_tokens_for_user
from core.utils.permissions import NotAuthenticate
from user.models import User



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


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (NotAuthenticate,)

    @swagger_auto_schema(
        operation_summary="login with password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
                "password" : openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=("phone","password")
        ),
        responses={
            200: LoginResponseSerializer
        }
    )
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # check phone
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        user = User.objects.filter(
            phone=phone
        ).only(
            "is_active", "is_staff", 'phone', 'password'
        ).first()
        if not user:
            raise NotFound("نام کاربری یا رمز عبور اشتباه هست")
        
        # check password
        password = user.check_password(password)
        if not password:
            raise NotFound("نام کاربری یا رمز عبور اشتباه هست")
        
        # create token
        token = get_tokens_for_user(user)
        data = {
            "token": token,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "expired_date": timezone.now() + timedelta(days=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days),
            "expire_timestamp": time.time() + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        }
        return Response(data=data)


class ActivateUserAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Activate User Account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING),
                "otp_code" : openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["phone","otp_code"],
        )
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
        

class ChangeUserPassword(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_summary="change password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "old_password" : openapi.Schema(type=openapi.TYPE_STRING),
                "new_password" : openapi.Schema(type=openapi.TYPE_STRING),
                "confirm_new_password" : openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=["password"],
        )
    )
    def post(self,request):
        # import ipdb
        # ipdb.set_trace()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # data
        old_passwod = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']

        # get user
        user = User.objects.filter(
            id=request.user.id
        ).only("password").first()
        if not user:
            raise NotFound("نام کاربری یا رمز عبور اشتباه هست")

        # check old password
        check_old_passwor = user.check_password(old_passwod)
        if not check_old_passwor:
            raise PasswordNotMatch()
        
        # check equal new_password and confrim_new_password
        if new_password != confirm_new_password:
            raise PasswordNotEqaul()
        
        # set new password
        user.set_password = confirm_new_password
        user.save()
        
        data = {
            "message": "پسورد شما با موفقیت تغییر یافت"
        }
        return Response(data=data)
 

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