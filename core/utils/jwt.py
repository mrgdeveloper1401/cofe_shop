from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils import timezone


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    expired_access_datetime = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    expire_refresh_datetime = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        "access_token_time": expired_access_datetime,
        "refresh_token_time": expire_refresh_datetime
    }
