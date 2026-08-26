from django.db import models
from academics.models import StudentClass
from departments.models import Department
from teachers.models import Teacher


from academics.models import Session,Section,StudentClass



class Subject(models.Model):

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE,
        related_name="subjects",
    )

    full_marks = models.PositiveIntegerField(
        default=100,
    )

    pass_marks = models.PositiveIntegerField(
        default=33,
    )

    credit = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
    )

    is_optional = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "student_class",
            "name",
        ]

        constraints = [

            models.UniqueConstraint(

                fields=[
                    "student_class",
                    "name",
                ],

                name="unique_subject_per_class",

            )

        ]

    def __str__(self):

        return f"{self.code} - {self.name}"


class SubjectAssignment(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE
    )

    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.subject} - {self.teacher}"