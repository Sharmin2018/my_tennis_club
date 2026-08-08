from django.db import models
from subjects.models import SubjectAssignment


class Routine(models.Model):

    DAY_CHOICES = [
        
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
    ]

    subject_assignment = models.ForeignKey(
        SubjectAssignment,
        on_delete=models.CASCADE,
        related_name="routines"
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    room = models.CharField(
        max_length=30
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "day",
            "start_time"
        ]

    def __str__(self):
        return f"{self.subject_assignment.subject} - {self.day}"