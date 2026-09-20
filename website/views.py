from django.shortcuts import render

from .models import HomeHero, AboutSection


def home(request):

    heroes = (
        HomeHero.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    about = (
        AboutSection.objects
        .filter(is_active=True)
        .first()
    )

    return render(
        request,
        "frontend/home.html",
        {
            "heroes": heroes,
            "about": about,
        }
    )