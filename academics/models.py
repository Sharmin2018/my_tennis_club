from django.db import models

class StudentClass(models.Model):

    name = models.CharField(
        max_length=30,
        unique=True,
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

class Session(models.Model):

    name = models.CharField(
        max_length=20,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
    
class Section(models.Model):

    name = models.CharField(
        max_length=10,
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class BloodGroup(models.Model):

    name = models.CharField(
        max_length=5,
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class School(models.Model):

    name = models.CharField(
        max_length=200,
    )

    eiin = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.CharField(
        max_length=250,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name