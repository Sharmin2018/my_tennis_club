from django.contrib import admin
from .models import PromotionHistory


@admin.register(PromotionHistory)
class PromotionHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "from_class",
        "to_class",
        "section",
        "promoted_by",
        "promoted_at",
    )

    search_fields = (
        "student__name",
    )

    list_filter = (
        "from_class",
        "to_class",
        "section",
    )