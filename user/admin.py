from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from user.models import User, UserNotification


admin.site.unregister(Group)


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "title", "is_active", "created_at", "updated_at")
    list_display_links = ("id", "user_id")
    list_filter = ("is_active", "created_at")
    list_per_page = 20
    search_fields = ("user__phone", "user__username")
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل و یا یوزرنیم استفاده کنید")
    raw_id_fields = ("user",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # form = CustomUserCreationForm
    list_display = ("id", "username", "email", "phone", "is_active", "is_superuser", "is_staff")
    list_editable = ("is_active",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_per_page = 20
    search_fields = ("username", "phone")
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل و ایمیل استفاده کنید")
    list_display_links = ("id", "username", "phone", "email")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("phone", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone", "username", "usable_password", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("updated_at", "created_at", "last_login")
    filter_horizontal = ()
