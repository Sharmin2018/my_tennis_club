from django.db import models


class NavigationMenu(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=False)

    @property
    def has_children(self):
        return self.children.filter(is_active=True).exists()

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class WebsiteSettings(models.Model):
    school_name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to="website/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.school_name


class HomeHero(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    background_image = models.ImageField(
        upload_to="website/hero/",
        blank=True,
        null=True
    )

    button_text = models.CharField(
        max_length=100,
        blank=True
    )

    button_url = models.CharField(
        max_length=255,
        blank=True
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    title = models.CharField(
        max_length=200,
        default="About Our School"
    )

    short_description = models.TextField()

    image = models.ImageField(
        upload_to="website/about/",
        blank=True,
        null=True
    )

    button_text = models.CharField(
        max_length=100,
        default="Read More"
    )

    button_url = models.CharField(
        max_length=255,
        default="/about/"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title