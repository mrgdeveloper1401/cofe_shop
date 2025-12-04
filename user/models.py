from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator,MaxLengthValidator


class User (AbstractBaseUser,PermissionsMixin) : 
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
