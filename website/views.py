
from django.shortcuts import render

from .models import HomeHero


def home(request):
    heroes = (
        HomeHero.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    return render(
        request,
        "frontend/home.html",
        {
            "heroes": heroes,
        }
    )