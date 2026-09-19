from .models import NavigationMenu, WebsiteSettings


def frontend_context(request):

    navigation_menus = (
        NavigationMenu.objects
        .filter(
            parent__isnull=True,
            is_active=True
        )
        .prefetch_related("children")
        .order_by("order", "name")
    )

    settings = WebsiteSettings.objects.first()

    return {
        "navigation_menus": navigation_menus,
        "school_name": settings.school_name if settings else "",
        "school_logo": settings.logo if settings else None,
    }