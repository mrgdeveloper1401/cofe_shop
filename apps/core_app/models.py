from django.db import models
from django.utils.translation import gettext_lazy as _



class ActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(CreateMixin, UpdateMixin, ActiveMixin):
    image  = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        help_text=_('Upload the original image file.'),
        null=True,
        verbose_name=_("عکس")
    )
    size = models.PositiveIntegerField(_("حجم عکس"), default=0)
    width = models.PositiveIntegerField(_("عرض"), default=0)
    height = models.PositiveIntegerField(_("ارتفاع"), default=0)
    image_id_ba_salam = models.BigIntegerField(
        blank=True,
        null=True,
        editable=False,
        help_text=_('ID of the image in external storage'),
        verbose_name=_("ای دی عکس اپلود شده درون با سلام")
    )
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        related_name="upload_images",
        verbose_name=_("کاربر")
    )

    @property
    def get_image_url(self):
        return self.image.url

    class Meta:
        db_table = 'core_app_image'

    def save(self, *args, **kwargs):
        self.size = self.image.size
        self.width = self.image.width
        self.height = self.image.height
        return super().save(*args, **kwargs)


class PublicNotification(ActiveMixin, CreateMixin, UpdateMixin):
    title = models.CharField(_("عنوان"), max_length=255)
    body = models.TextField(_("متن نوتیفکیشن"))
    
    class Meta:
        db_table = "public_notification"
