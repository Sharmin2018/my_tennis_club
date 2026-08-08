
from django.db import models
from departments.models import Department
from django.utils import timezone
from academics.models import (
    Session,
    StudentClass,
    Section,
    BloodGroup, 
)

from members.models import Student


class AdmissionApplication(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Verified", "Verified"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    RELIGION_CHOICES = [
        ("Islam", "Islam"),
        ("Hindu", "Hindu"),
        ("Buddhist", "Buddhist"),
        ("Christian", "Christian"),
        ("Other", "Other"),
    ]

    # Admission Information

    application_id = models.CharField(
        max_length=30,
        unique=True,
    )
    

    admission_session = models.ForeignKey(
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
        on_delete=models.PROTECT,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    # Student Information

    name = models.CharField(max_length=150)

    father_name = models.CharField(max_length=150)

    mother_name = models.CharField(max_length=150)

    dob = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    religion = models.CharField(
        max_length=20,
        choices=RELIGION_CHOICES,
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


    previous_school = models.CharField(
    max_length=200,
    blank=True,
    )
    # Contact

    phone = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
    )

    present_address = models.TextField()

    permanent_address = models.TextField()

    # Guardian

    guardian_name = models.CharField(max_length=150)

    guardian_phone = models.CharField(max_length=20)

    guardian_occupation = models.CharField(
        max_length=100,
        blank=True,
    )

    # Documents

    photo = models.ImageField(
        upload_to="admission/photos/",
    )

    birth_certificate = models.FileField(
        upload_to="admission/documents/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        if not self.application_id:

            year = timezone.now().year

            last_application = AdmissionApplication.objects.filter(
                application_id__startswith=f"ADM-{year}"
            ).order_by("-id").first()

            if last_application:
                last_number = int(
                    last_application.application_id.split("-")[-1]
                ) + 1
            else:
                last_number = 1

            self.application_id = (f"ADM-{year}-{last_number:06d}")

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.application_id} - {self.name}"

    def create_student(self, user):

        student = Student.objects.create(

            created_by=user,

            name=self.name,

            father_name=self.father_name,
            mother_name=self.mother_name,

            dob=self.dob,
            gender=self.gender,
            religion=self.religion,

            blood_group=self.blood_group,
            nationality=self.nationality,

            session=self.admission_session,
            student_class=self.student_class,
            section=self.section,
            department=self.department,

            phone=self.phone,
            email=self.email,

            present_address=self.present_address,
            permanent_address=self.permanent_address,

            previous_school=self.previous_school,

            guardian_name=self.guardian_name,
            guardian_phone=self.guardian_phone,
            guardian_occupation=self.guardian_occupation,

            photo=self.photo,
        )

        self.status = "Approved"
        self.save()

        return student

   