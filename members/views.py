
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.db.models import Q

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import StudentForm
from .models import Student

from core.mixins import UserCreateMixin,SuccessMessageMixin,BaseListMixin
from departments.models import Department
from academics.models import (
    StudentClass,
    Section,
)



# -------------------------
# Student List
# -------------------------
class StudentListView(LoginRequiredMixin, PermissionRequiredMixin,BaseListMixin, ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    login_url = '/login/'
    
    permission_required = "members.view_student"
    

    def get_queryset(self):

        query = self.request.GET.get("q")

        student_class = self.request.GET.get("class")

        section = self.request.GET.get("section")

        gender = self.request.GET.get("gender")

        queryset = Student.objects.all()
        department = self.request.GET.get("department")

        if query:

            queryset = queryset.filter(

            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(roll__icontains=query) |
            Q(registration_no__icontains=query)

        )
            

        if department:

            queryset = queryset.filter(
            department_id=department
        )
        if gender:

            queryset = queryset.filter(
            gender=gender
        )

        if student_class:

            queryset = queryset.filter(
            student_class=student_class
        )

        if section:

            queryset = queryset.filter(
            section=section
        )

        return queryset.order_by(*self.ordering)
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["classes"] = StudentClass.objects.all()

        context["sections"] = Section.objects.all()

        context["departments"] = Department.objects.all()

        return context
    
    

# -------------------------
# Add Student
# -------------------------
class StudentCreateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        UserCreateMixin,
                        SuccessMessageMixin,
                        CreateView):
    
    model = Student

    form_class = StudentForm

    template_name = "student_form.html"

    success_url = reverse_lazy("student_list")

    permission_required = "members.add_student"

    success_message = "Student added successfully."
    login_url = 'login'
    permission_required = "members.add_student"

   
# -------------------------
# Edit Student
# -------------------------
class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
   
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_list")
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
class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
     model = Student
     template_name = "delete.html"
     success_url = reverse_lazy("student_list")
     login_url = "/login/"
     pk_url_kwarg = "id"
     permission_required = "members.delete_student"
     success_message = "Student deleted successfully."

     

    
# -------------------------
# Detail View
# -------------------------

class StudentDetailView(LoginRequiredMixin, DetailView):
        model = Student
        template_name = "student_detail.html"
        context_object_name = "student"
        pk_url_kwarg = "id"

# -------------------------
# Detail print
# -------------------------

class StudentPrintView(DetailView):
    model = Student
    template_name = "student_print.html"
    context_object_name = "student"

