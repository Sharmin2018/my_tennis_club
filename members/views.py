from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View,DetailView,TemplateView
from .forms import StudentForm
from .models import Student
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.mixins import UserCreateMixin




# -------------------------
# Student List
# -------------------------
class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'list.html'
    context_object_name = 'students'
    login_url = '/login/'

    paginate_by = 3
    ordering = ['-id']
    permission_required = "members.view_student"

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Student.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(roll__icontains=query) |
                Q(registration_no__icontains=query)
            ).order_by('-id')

        return Student.objects.all().order_by('-id')
    


# -------------------------
# Add Student
# -------------------------
class StudentCreateView(LoginRequiredMixin,PermissionRequiredMixin,UserCreateMixin,CreateView):
    model = Student

    form_class = StudentForm

    template_name = "student_form.html"

    success_url = reverse_lazy("list")

    permission_required = "members.add_student"

    success_message = "Student added successfully."
    login_url = '/login/'
    permission_required = "members.add_student"

   
# -------------------------
# Edit Student
# -------------------------
class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
   
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("list")
    success_message = "Student updated successfully."
    pk_url_kwarg = "id"
    permission_required = "members.change_student"

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        if not self.request.user.is_superuser:
            form.fields["registration_no"].disabled = True

        return form

# -------------------------
# Delete Student
# -------------------------
class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
     model = Student
     template_name = "delete.html"
     success_url = reverse_lazy("list")
     login_url = "/login/"
     pk_url_kwarg = "id"
     permission_required = "members.delete_student"

     def form_valid(self, form):
        messages.success(
            self.request,
            "Student deleted successfully."
        )
        return super().form_valid(form)

# -------------------------
# Register
# -------------------------
class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')
    
# -------------------------
# Detail View
# -------------------------

class StudentDetailView(LoginRequiredMixin, DetailView):
        model = Student
        template_name = "student_detail.html"
        context_object_name = "student"
        pk_url_kwarg = "id"

# -------------------------
# Dashboard View
# -------------------------

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["student_count"] = Student.objects.count()

        context["male_students"] = Student.objects.filter(
        gender="Male"
        ).count()

        context["female_students"] = Student.objects.filter(
        gender="Female"
         ).count()

        context["photo_students"] = Student.objects.exclude(
        photo=""
        ).count()

        return context