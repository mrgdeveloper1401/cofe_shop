from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core_app.models import ActiveMixin, CreateMixin, UpdateMixin, Image


class HeaderSite(ActiveMixin, UpdateMixin, CreateMixin):
    title = models.CharField(_("عنوان هدر"), max_length=30)
    
    class Meta:
        db_table = "header_site"


class SliderConfig(CreateMixin, UpdateMixin, ActiveMixin):
    class Meta:
        db_table = "slider_config"


class SlideBox(CreateMixin, UpdateMixin, ActiveMixin):
    slider = models.ForeignKey(
        to=SliderConfig,
        on_delete=models.PROTECT,
        related_name="boxes",
        verbose_name=_("اسلایدر"),
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        related_name="slider_box_images",
        verbose_name=_("عکس باکس"),
    )
    title =  models.CharField(_("عنوان عکس"), max_length=256)
    link = models.CharField(_("لینک عکس"), default="/",max_length=256)

    class Meta:
        db_table = "slider_box"


class SlideImage(CreateMixin, UpdateMixin, ActiveMixin):
    slider = models.ForeignKey(
        to=SliderConfig,
        on_delete=models.PROTECT,
        related_name="images",
        verbose_name=_("اسلایدر")
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        related_name="slider_images",
        verbose_name=_("عکس اسلایدر"),
    )

    class Meta:
        db_table = "slider_image"


class Footer(CreateMixin, UpdateMixin, ActiveMixin):
    instagram_page = models.CharField(_(""), max_length=128,null=True,blank=True)
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
