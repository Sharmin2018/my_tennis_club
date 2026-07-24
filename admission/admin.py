
from django.contrib import admin
from .models import AdmissionApplication

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "application_id",
        "name",
        "student_class",
        "department",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "student_class",
        "department",
        "admission_session",
    )

    search_fields = (
        "application_id",
        "name",
        "phone",
    )

    ordering = ("-created_at",)
