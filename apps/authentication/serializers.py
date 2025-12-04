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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","phone")


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    phone = serializers.CharField(validators=(PHONE_VALIDATOR,))


class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
