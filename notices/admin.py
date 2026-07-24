from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "publish_date",
        "created_by",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "publish_date",
        "created_at",
    )

    ordering = (
        "-publish_date",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )