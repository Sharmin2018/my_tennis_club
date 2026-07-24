from django.db import models
from academics.models import StudentClass, Section
from django.conf import settings
from members.models import Student

class PromotionHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )

    from_class = models.ForeignKey(
        StudentClass,
        on_delete=models.PROTECT,
        related_name="from_class_promotions",
    )

    to_class = models.ForeignKey(
        StudentClass,
        on_delete=models.PROTECT,
        related_name="to_class_promotions",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
    )

    promoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    promoted_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.student.name} ({self.from_class} → {self.to_class})"