from django.contrib import admin
from .models import NavigationMenu, WebsiteSettings, HomeHero, AboutSection
   


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "url",
        "order",
        "is_active",
        "open_new_tab",
    )
    list_filter = ("is_active", "parent")
    search_fields = ("name", "url")
    ordering = ("order", "name")


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("school_name",)


@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "subtitle",
    )

    ordering = (
        "order",
        "id",
    )

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "short_description",
    )