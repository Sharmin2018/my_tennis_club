from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "photo_preview",
        "name",
        "designation",
        "department",
        "email",
        "phone",
        "joining_date",
        "created_by",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "designation",
        "department",
    )

    list_filter = (
        "department",
        "gender",
        "religion",
    )

    ordering = ("-id",)

    list_per_page = 10

    
    readonly_fields = (
    "created_by",
    "photo_preview",
)

    fieldsets = (
        ("Personal Information", {
            "fields": (
                "name",
                "photo",
                "dob",
                "gender",
                "religion",
            )
        }),
        ("Professional Information", {
            "fields": (
                "designation",
                "department",
                "joining_date",
            )
        }),
        ("Contact", {
            "fields": (
                "email",
                "phone",
            )
        }),
        ("System", {
            "fields": (
                "created_by",
            )
        }),
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:

            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    def photo_preview(self, obj):

        if obj.photo:

            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;">',
                obj.photo.url
            )

        return "No Photo"

    photo_preview.short_description = "Photo"