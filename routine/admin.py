from django.contrib import admin
from .models import Routine, Period


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "name",
        "start_time",
        "end_time",
        "is_active",
    )


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = (
        "day",
        "period",
        "subject_assignment",
        "room",
        "is_active",
    )

    list_filter = (
        "day",
        "period",
        "is_active",
    )

    search_fields = (
        "subject_assignment__subject__name",
        "subject_assignment__subject__code",
        "subject_assignment__teacher__name",
        "room",
    )

    list_select_related = (
        "period",
        "subject_assignment",
    )