from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
app = Celery("core")

app.conf.update(
    timezone="Asia/Tehran",
    enable_utc=True,
)


# calculate similar product every 24 hour
# app.conf.beat_schedule = {
#     "calculate_similar_products" : {
#         "task" : "apps.product.tasks.calculate_similar_products",
#         "schedule" : 60 * 60 * 24
#     }
# }


app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks()