from django.core.cache import cache
from rest_framework import views, response

from apps.template import serializers
from apps.template import models


class HeaderSiteView(views.APIView):
    serializer_class = serializers.HeaderSiteSerializer

    def get(self, request):
        # get cache
        get_value =cache.get("header_site")
        if get_value:
            return response.Response(get_value)

        # query and serializer data
        queryset = models.HeaderSite.objects.filter(is_active=True).only("title")
        serializer = self.serializer_class(queryset, many=True)

        # set cache
        cache.set("header_site", serializer.data, timeout=60 * 60 * 24 * 30)

        # response data
        return response.Response(serializer.data)


class SliderBoxView(views.APIView):
    serializer_class = serializers.SlideBoxSerializer

    def get(self, request):
        # get cache 
        get_value = cache.get("slider_box")
        if get_value:
            return response.Response(get_value)

        queryset = models.SlideBox.objects.filter(is_active=True).select_related("image").only(
            "title",
            "link",
            "image__image"
        )
        serializer = self.serializer_class(queryset, many=True)
        
        # set cache
        cache.set("slider_box", serializer.data, timeout=60 * 60 * 24 * 30)
        
        # response data
        return response.Response(serializer.data)


class SliderImageView(views.APIView):
    serializer_class = serializers.SlideImageSerializer

    def get(self, request):
        # get cache
        get_cache = cache.get("slider_image")
        if get_cache:
            return response.Response(get_cache)

        queryset = models.SlideImage.objects.filter(is_active=True).select_related("image").only("image__image")
        serializer = self.serializer_class(queryset, many=True)

        # set cache
        cache.set("slider_image", serializer.data, timeout=60 * 60 * 24 * 30)
        return response.Response(serializer.data)
