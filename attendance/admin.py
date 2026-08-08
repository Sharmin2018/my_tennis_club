from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "date",
        "status",
        "taken_by",
    )

    list_filter = (
        "date",
        "status",
    )

    search_fields = (
        "student__name",
        "student__roll",
    )