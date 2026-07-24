from django.db import models
from django.contrib.auth.models import User


class Notice(models.Model):

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    notice_file = models.FileField(
        upload_to="notices/",
        blank=True,
        null=True
    )

    publish_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-publish_date"]

        verbose_name = "Notice"

        verbose_name_plural = "Notices"

    def __str__(self):

        return self.title