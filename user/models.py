from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.utils.translation import gettext_lazy as _

from apps.core_app.models import ActiveMixin, CreateMixin, UpdateMixin


class User(AbstractBaseUser, PermissionsMixin, CreateMixin, UpdateMixin):
    username = models.CharField(max_length=300,unique=True)
    phone = models.SlugField(
        max_length=11,
        validators=[
            MinLengthValidator(11),
            MaxLengthValidator(15),
        ],
        unique=True,
        )
    email = models.EmailField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ("phone", "email")

    objects = UserManager()

    class Meta : 
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserNotification(CreateMixin, UpdateMixin, ActiveMixin):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="user_notifications",
        verbose_name=_("کاربر")
    )
    title = models.CharField(_("عنوان"), max_length=255)
    body = models.TextField(_("متن نوتیفکیشن"))
    
    class Meta:
        db_table = "user_notifications"
