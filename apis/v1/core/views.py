from rest_framework import mixins, viewsets

from apis.v1.core import serializers
from apps.core_app.models import PublicNotification
from core.utils.paginations import ScrollPagination



class PublicNotificationView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PublicNotificationSerializer
    pagination_class = ScrollPagination

    def get_queryset(self):
        return PublicNotification.objects.filter(is_active=True).only("title", "created_at", "body")
