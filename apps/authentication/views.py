from datetime import timedelta
import datetime
import secrets
import time

from django.core.cache import cache
from django.utils import timezone
from rest_framework import views, response, exceptions, status, permissions, mixins, viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.authentication import serializers
from core.settings import SIMPLE_JWT
from apps.authentication.tasks import send_otp
from core.utils import exceptions as custom_exception
from core.utils import response as custom_response
from core.utils.jwt import get_tokens_for_user
from core.utils.paginations import ScrollPagination
from core.utils.permissions import NotAuthenticate
from core.utils.user_ip import user_ip
from user import models
from user.models import User


class RegisterAPIView(views.APIView):
    serializer_class = serializers.RegisterSerializer
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
        return response.Response(data=data, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    serializer_class = serializers.LoginSerializer
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
            200: serializers.LoginResponseSerializer
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
            raise exceptions.NotFound("نام کاربری یا رمز عبور اشتباه هست")
        
        # check password
        password = user.check_password(password)
        if not password:
            raise exceptions.NotFound("نام کاربری یا رمز عبور اشتباه هست")
        
        # create token
        token = get_tokens_for_user(user)
        data = {
            "token": token,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "expired_date": timezone.now() + timedelta(days=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days),
            "expire_timestamp": time.time() + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        }
        return response.Response(data=data)


class ChangeUserPassword(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

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
            raise exceptions.NotFound("نام کاربری یا رمز عبور اشتباه هست")

        # check old password
        check_old_passwor = user.check_password(old_passwod)
        if not check_old_passwor:
            raise custom_exception.PasswordNotMatch()
        
        # check equal new_password and confrim_new_password
        if new_password != confirm_new_password:
            raise custom_exception.PasswordNotEqaul()
        
        # set new password
        user.set_password = confirm_new_password
        user.save()
        
        data = {
            "message": "پسورد شما با موفقیت تغییر یافت"
        }
        return response.Response(data=data)
 

class RequestPhoneforgetPasswordView(views.APIView):
    serializer_class = serializers.RequestForgetPasswordSerializer
    permission_classes = (NotAuthenticate,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # phone
        phone = serializer.validated_data['phone']

        # check user exists
        user = User.objects.filter(phone=phone).only("phone", "is_active").first()
        if not user:
            raise custom_exception.UserNotFound()
        if user.is_active is False:
            raise custom_exception.UserNotActive()

        # set in redis
        otp = secrets.randbelow(1_000_000)
        ip = user_ip(request)
        redis_key = f'forget_password_{user.phone}_{otp}_{ip}'
        cache.set(redis_key, otp, timeout=120)
        # send otp
        
        # response data
        data = {
            "expired_time": timezone.now() + datetime.timedelta(minutes=2),
            "expire_timestamp": time.time() + datetime.timedelta(seconds=120).total_seconds()
        }
        message = "پردازش با موفقیت انجام شد"
        return custom_response.api_response(data=data, message=message)


class VerifyRequestPhoneforgetPasswordView(views.APIView):
    serializer_class = serializers.VerifyRequestForgetPasswordSerializer
    permission_classes = (NotAuthenticate,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # get data
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']
        
        # check user
        user = User.objects.filter(phone=phone).only("password", "phone", "is_active").first()
        if not user:
            raise custom_exception.UserNotFound()
        if user.is_active is False:
            raise custom_exception.UserNotActive()
        
        # check password
        if new_password != confirm_new_password:
            raise custom_exception.PasswordNotEqaul()
        
        # save new password
        user.set_password(confirm_new_password)
        user.save()
        
        # check otp
        ip = user_ip(request)
        redis_key = f'forget_password_{user.phone}_{otp}_{ip}'
        check_otp = cache.get(redis_key)
        if not check_otp:
            raise custom_exception.OtpNotFound()
        
        # remove otp code in redis
        cache.delete(redis_key)
        
        # new token
        token = get_tokens_for_user(user)
        
        # response data
        message = "پردازش با موفقییت انجام شد"
        return custom_response.api_response(data=token, message=message)


class UserNotificationView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserNotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = ScrollPagination

    def get_queryset(self):
        return models.UserNotification.objects.filter(
            user_id=self.request.user.id
        ).only("title", "created_at", "body")
