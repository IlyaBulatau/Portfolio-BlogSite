from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Tag, IPView


@admin.register(Post)
class PostAdminCustom(admin.ModelAdmin):
    readonly_fields = ("slug", "views")
    list_display = (
        "pk",
        "slug",
        "user",
        "created_on",
    )
    list_display_links = (
        "pk",
        "slug",
    )
    list_filter = ("author", "created_on")
    search_fields = ("pk", "title__startswith")
    ordering = ("-pk",)

    def user(self, obj):
        link = reverse("admin:users_user_change", args=[obj.author.pk])
        return format_html('<a href="{}">{}</a>', link, obj.author.username)


@admin.register(Tag)
class TagAdminCustom(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    readonly_fields = ("slug",)
    search_fields = ("name__startswith",)

    add_fieldsets = (
        (
            _("Tag"),
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "description",
                ),
            },
        ),
    )

@admin.register(IPView)
class IPViewAdminCustom(admin.ModelAdmin):
    list_display = (
        "address",
    )
