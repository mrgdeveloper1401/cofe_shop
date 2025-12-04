from django.urls import path
from apps.template import api


urlpatterns = [

    path("index/",api.IndexAPIView.as_view(),name="index"),

    path("layout/",api.LayoutAPIView.as_view(),name="layout"),

]