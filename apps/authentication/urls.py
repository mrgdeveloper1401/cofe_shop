from django.urls import path
from apps.authentication import api
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("v1/register/", api.RegisterAPIView.as_view(), name="register"),
    # path("v1/activate/", api.ActivateUserAPIView.as_view(), name="activate"),
    path("v1/change-password/", api.ChangeUserPassword.as_view(), name="change-password"),
    # path("v1/token/refresh/",TokenRefreshView.as_view(),name="refresh-token"),
    path("v1/login/", api.LoginAPIView.as_view(), name="login"),
    # path("v1/send-otp/", api.SendOptCodeAPIView.as_view(), name="send-otp"),
]
