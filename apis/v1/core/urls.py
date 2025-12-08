from rest_framework import routers

from apis.v1.core import views

app_name = "v1_core"

router = routers.SimpleRouter()
router.register("public_notification", views.PublicNotificationView, basename="public_notification")

urlpatterns = [
    
] + router.urls
