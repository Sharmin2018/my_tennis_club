
from django.db import models

from django.db import models


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

    # Basic Information
    name = models.CharField(max_length=100)
    roll = models.PositiveIntegerField(unique=True)
    registration_no = models.CharField(max_length=30, unique=True)

    # Academic Information
    session = models.CharField(max_length=20)
    student_class = models.CharField(max_length=20)

    # Contact Information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    # Personal Information
    dob = models.DateField()
    religion = models.CharField(
        max_length=20,
        choices=RELIGION_CHOICES
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    # Photo
    photo = models.ImageField(
        upload_to='student_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
   