
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from departments.models import Department


class Staff(models.Model):

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

    DESIGNATION_CHOICES = [
        ("Office Superintendent", "Office Superintendent"),
        ("Accountant", "Accountant"),
        ("Cashier", "Cashier"),
        ("Office Assistant", "Office Assistant"),
        ("Computer Operator", "Computer Operator"),
        ("Store Keeper", "Store Keeper"),
        ("Library Assistant", "Library Assistant"),
        ("Lab Assistant", "Lab Assistant"),
        ("Lab Attendant", "Lab Attendant"),
        ("Driver", "Driver"),
        ("Security Guard", "Security Guard"),
        ("Office Support Staff", "Office Support Staff"),
        ("Cleaner", "Cleaner"),
    ]

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    designation = models.CharField(
        max_length=50,
        choices=DESIGNATION_CHOICES
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^01[3-9]\d{8}$',
                message='Enter a valid Bangladeshi phone number.'
            )
        ]
    )

    dob = models.DateField()

    joining_date = models.DateField()

    religion = models.CharField(
        max_length=20,
        choices=RELIGION_CHOICES
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    photo = models.ImageField(
        upload_to="staff_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name