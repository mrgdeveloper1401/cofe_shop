import re
from rest_framework import serializers
from apps.authentication.validators import PHONE_VALIDATOR
from user.models import User

# Password regex: must contain uppercase, lowercase, and numeric characters
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    phone = serializers.CharField(validators=(PHONE_VALIDATOR,))

    class Meta:
        model = User
        fields = ("username","phone","password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","phone")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    phone = serializers.CharField(validators=(PHONE_VALIDATOR,))


class RequestForgetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=(PHONE_VALIDATOR,))


class VerifyRequestForgetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=(PHONE_VALIDATOR,))
    otp = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()


class tokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    token = tokenResponseSerializer()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    expired_date = serializers.DateTimeField()
    expire_timestamp = serializers.FloatField()
