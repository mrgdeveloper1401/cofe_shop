from django.db import models
import uuid

from apps.core_app.models import ActiveMixin


class SliderConfig(models.Model):
    is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "slider_config"


class SlideBox(models.Model):
    slider = models.ForeignKey(
        to=SliderConfig,
        on_delete=models.PROTECT,
        related_name="boxes",
    )
    image_url = models.ImageField(upload_to="media/template/slider/slide-box")
    title =  models.CharField(max_length=256)
    link = models.CharField(default="/",max_length=256)

    class Meta:
        db_table = "slider_box"


class SlideImage(models.Model):
    slider = models.ForeignKey(
        to=SliderConfig,
        on_delete=models.PROTECT,
        related_name="images",
    )
    image_url = models.ImageField(upload_to="media/template/slider/slides")

    class Meta:
        db_table = "slider_image"


class Footer(ActiveMixin):
    instagram_page = models.CharField(max_length=128,null=True,blank=True)
    telegram_channel = models.CharField(max_length=128,null=True,blank=True)
    whatsapp_support = models.CharField(max_length=128,null=True,blank=True)
    phone = models.CharField(max_length=13,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.CharField(max_length=256,null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table = "footer"
    

class License(models.Model):
    footer = models.ForeignKey(
        to=Footer,
        on_delete=models.PROTECT,
        related_name="licenses",
    )
    image = models.ImageField(upload_to="template/footer/license/")
    url = models.CharField(max_length=256)

    class Meta:
        db_table = "license"


class GrouLinkFooter(models.Model):
    footer = models.ForeignKey(
        to=Footer,
        on_delete=models.PROTECT,
        related_name="group_links",
    )
    title = models.CharField(max_length=128)

    class Meta:
        db_table = "grou_link_footer"


class FooterLink(models.Model):
    group_link = models.ForeignKey(
        to=GrouLinkFooter,
        on_delete=models.PROTECT,
        related_name="links",
    )
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=256,)

    class Meta:
        db_table = "footer_link"
