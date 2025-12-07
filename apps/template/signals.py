from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache

from apps.template import models


@receiver([post_save, post_delete], sender=models.HeaderSite)
def clear_cache(*args, **kwargs):
    cache.delete("header_site")


@receiver([post_save, post_delete], sender=models.SlideBox)
def clear_cache(*args, **kwargs):
    cache.delete("slider_box")
