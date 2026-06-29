from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required(login_url='/login/')

def student_list(request):
    print("USER:", request.user)
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'list.html', {'students': students})

@login_required(login_url='/login/')
def add_student(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        Student.objects.create(name=name, email=email, age=age)
        return redirect('list')
    return render(request, 'add.html')

@login_required(login_url='/login/')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.age = request.POST['age']
        student.save()
        return redirect('list')
    return render(request, 'edit.html', {'student': student})

@login_required(login_url='/login/')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('list')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')