from django.urls import path
from apps.authentication import api
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/",api.RegisterAPIView.as_view(),name="register"),

    path("activate/",api.ActivateUserAPIView.as_view(),name="activate"),

    path("change-password/",api.ChangeUserPassword.as_view(),name="change-password"),

    path("token/refresh/",TokenRefreshView.as_view(),name="refresh-token"),

    path("login/",api.LoginAPIView.as_view(),name="login"),

    path("send-otp/",api.SendOptCodeAPIView.as_view(),name="send-otp"),
]