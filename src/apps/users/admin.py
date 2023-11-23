from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Contact
from .models import User


class Contactinline(admin.StackedInline):
    model = Contact
    

@admin.register(User)
class UserAdminCustom(UserAdmin):
    
    list_display = ("email", "pk", "username", "profile", "is_staff")
    list_filter = ("created_on", "last_login", "is_staff", "is_active")
    list_display_links = ("email", "pk")
    list_editable = ("is_staff", )
    search_fields = ("username__startswith", )
    ordering = ("pk", )
    readonly_fields = ("slug", )
    inlines = (Contactinline, )
    # add show user avatar
    
    def profile(self, obj):
        link = reverse("profile_detail_view", args=(obj.slug, ))
        return format_html(f"<a href='{link}'>link</a>")
    

    fieldsets = (
        (_("Register info"), {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "slug", "about", "avatar")}),
        (
            _("Permissions"),
            {
                "classes": ["collapse"],
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            _("Requirement"),
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            }
        ),
        (
            _("Additionaly"),
            {
                "fields": ("first_name", "last_name", "about", "avatar", "is_staff", "user_permissions")
            }
        ),
    )
