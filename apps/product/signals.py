from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache

from apps.product import models


@receiver([post_save, post_delete], sender=models.ProductCategory)
def clear_cache(*args, **kwargs):
    cache.delete("parent_category")
