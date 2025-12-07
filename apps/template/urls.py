from django.urls import path
from apps.template import views


app_name = "v1_template"

urlpatterns = [
    path("header_site/", views.HeaderSiteView.as_view(), name='header_site'),
    path("slider_box/", views.SliderBoxView.as_view(), name='slider_box'),
    path("slider_images/", views.SliderImageView.as_view(), name="slider_images"),
    path("index/", views.IndexAPIView.as_view(), name="index"),
    path("layout/", views.LayoutAPIView.as_view(), name="layout"),

]
