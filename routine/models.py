from django.db import models
from django.core.exceptions import ValidationError

from subjects.models import SubjectAssignment


class Period(models.Model):

    number = models.PositiveIntegerField(
        unique=True
    )

    name = models.CharField(
        max_length=50
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.start_time.strftime('%H:%M')} - "
            f"{self.end_time.strftime('%H:%M')})"
        )


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

    period = models.ForeignKey(
        Period,
        on_delete=models.PROTECT,
        related_name="routines",
        null=True,
        blank=True,
    )

    

    room = models.CharField(
        max_length=30
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "day",
            "period__number"
        ]

    def __str__(self):
        return f"{self.subject_assignment.subject} - {self.day}"

    def clean(self):

        if not self.period:
            return

        # ==========================================
        # Current class information
        # ==========================================

        assignment = self.subject_assignment

        current_class = assignment.student_class
        current_section = assignment.section
        current_teacher = assignment.teacher

        # ==========================================
        # 1. SAME SECTION / CLASS
        # ==========================================

        section_conflict = Routine.objects.filter(
            day=self.day,
            period=self.period,
            subject_assignment__student_class=current_class,
            subject_assignment__section=current_section,
            is_active=True,
        ).exclude(
            pk=self.pk
        )

        if section_conflict.exists():

            raise ValidationError(
                "This section already has a class in this period."
            )

        # ==========================================
        # 2. SAME TEACHER
        # ==========================================

        teacher_conflict = Routine.objects.filter(
            day=self.day,
            period=self.period,
            subject_assignment__teacher=current_teacher,
            is_active=True,
        ).exclude(
            pk=self.pk
        )

        if teacher_conflict.exists():

            raise ValidationError(
                f"{current_teacher} already has another class "
                f"in this period."
            )

        # ==========================================
        # 3. SAME ROOM
        # ==========================================

        room_conflict = Routine.objects.filter(
            day=self.day,
            period=self.period,
            room__iexact=self.room.strip(),
            is_active=True,
        ).exclude(
            pk=self.pk
        )

        if room_conflict.exists():

            raise ValidationError(
                f"Room {self.room} is already occupied "
                f"in this period."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)