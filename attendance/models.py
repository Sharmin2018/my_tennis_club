from django.db import models
from django.conf import settings
from members.models import Student


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
        ("Leave", "Leave"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )

    remarks = models.CharField(
        max_length=200,
        blank=True,
    )

    taken_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ["-date"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance"
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date}"