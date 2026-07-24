
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from departments.models import Department
from django.utils import timezone
from academics.models import (
    Session,
    StudentClass,
    Section,
    BloodGroup,
)


# Student Model
class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    RELIGION_CHOICES = [
        ('Islam', 'Islam'),
        ('Hindu', 'Hindu'),
        ('Buddhist', 'Buddhist'),
        ('Christian', 'Christian'),
        ('Other', 'Other'),
    ]

    
    
    
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    )

    name = models.CharField(max_length=100)
    
    roll = models.PositiveIntegerField(
    blank=True,
    null=True,
    )

    registration_no = models.CharField(
    max_length=30,
    unique=True,
    blank=True,
    )
    

    # Academic Information
    
    student_id = models.CharField(
    max_length=20,
    unique=True,
    blank=True,
    editable=False,
    )

    session = models.ForeignKey(
    Session,
    on_delete=models.PROTECT,
    )

    student_class = models.ForeignKey(
    StudentClass,
    on_delete=models.PROTECT,
    )

    section = models.ForeignKey(
    Section,
    on_delete=models.PROTECT,
    )

    department = models.ForeignKey(
    Department,
    on_delete=models.PROTECT
    )

   

    # Contact Information
    email = models.EmailField(
    blank=True,
    null=True,
    )
    
    phone = models.CharField(max_length=11,
                             validators=[RegexValidator(regex=r'^01[3-9]\d{8}$',
                             message='Enter a valid Bangladeshi phone number.'
                              )
                              ]
                              )
    present_address = models.TextField()

    permanent_address = models.TextField()

    # Personal Information
    father_name = models.CharField(max_length=150)

    mother_name = models.CharField(max_length=150)
    dob = models.DateField()
    religion = models.CharField(
        max_length=20,
        choices=RELIGION_CHOICES
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    blood_group = models.ForeignKey(
        BloodGroup,
        on_delete=models.PROTECT,
        null=True,
     blank=True,
    )

    nationality = models.CharField(
        max_length=50,
        default="Bangladeshi",
    )

    # Photo
    photo = models.ImageField(
        upload_to='student_images/',
        blank=True,
        null=True
    )

  # Previous school info
  
    previous_school = models.CharField(
    max_length=200,
    blank=True,
    )

    # Guardian info

    guardian_name = models.CharField(
    max_length=150,
    )

    guardian_phone = models.CharField(
    max_length=11,
    validators=[
        RegexValidator(
            regex=r"^01[3-9]\d{8}$",
            message="Enter a valid Bangladeshi phone number."
        )
        ]
    )

    guardian_occupation = models.CharField(
    max_length=100,
    blank=True,
    )
#----------------------------
    created_at = models.DateTimeField(
    auto_now_add=True,
    )

    updated_at = models.DateTimeField(
    auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=[
                "session",
                "student_class",
                "section",
                "department",
                "roll",
            ],
            name="unique_student_roll",
        )
        ]


    def __str__(self):
        return f"{self.student_id} - {self.name}"
    
    
    def save(self, *args, **kwargs):
        year = timezone.now().year

        if not self.student_id:

            last_student = Student.objects.filter(
               student_id__startswith=f"STU-{year}"
            ).order_by("-id").first()

            if last_student:

                last_number = int(
                  last_student.student_id.split("-")[-1]
                ) + 1

            else:

                last_number = 1

            self.student_id = (
                f"STU-{year}-{last_number:06d}"
            )

        if not self.roll:

            last_roll = Student.objects.filter(
            session=self.session,
            student_class=self.student_class,
            section=self.section,
            department=self.department,
            ).order_by("-roll").first()

            if last_roll:
                self.roll = last_roll.roll + 1
            else:
                self.roll = 1


        if not self.registration_no:

            last = Student.objects.filter(
                registration_no__startswith=f"REG-{year}"
            ).order_by("-id").first()

            if last:
                number = int(last.registration_no.split("-")[-1]) + 1
            else:
                number = 1

            self.registration_no = f"REG-{year}-{number:06d}"

        super().save(*args, **kwargs)
   