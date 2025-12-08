from django.urls import path
from rest_framework import routers

from apps.authentication import views


router = routers.SimpleRouter()
router.register("user_notification", views.UserNotificationView, basename="user_notification")

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("change-password/", views.ChangeUserPassword.as_view(), name="change-password"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("request_phone_forget_password/", views.RequestPhoneforgetPasswordView.as_view(), name='request_otp_phone'),
    path("verify_forget_password_phone/", views.VerifyRequestPhoneforgetPasswordView.as_view(), name='verify_forget_password_phone')
] + router.urls
