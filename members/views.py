from django.shortcuts import render
from .models import Student

def home(request):
    if request.method == "POST":
        name = request.POST.get("username")
        Student.objects.create(name=name)

    students = Student.objects.all()

    return render(request, "home.html", {"students": students})