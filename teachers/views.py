from django.db.models import Q
from django.views.generic import ListView
from .models import Teacher
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import TeacherForm
from core.mixins import UserCreateMixin


class TeacherListView(LoginRequiredMixin,ListView):

    model = Teacher

    template_name = "teacher_list.html"

    context_object_name = "teachers"

    paginate_by = 3

    def get_queryset(self):

        query = self.request.GET.get("q")

        queryset = Teacher.objects.all()

        if query:

            queryset = queryset.filter(

            Q(name__icontains=query) |

            Q(email__icontains=query) |

            Q(phone__icontains=query) |

            Q(designation__icontains=query)

        )

        return queryset.order_by("-id")

#----------------------------------------------------------------------------------

class TeacherCreateView( LoginRequiredMixin,PermissionRequiredMixin, UserCreateMixin,CreateView):

    model = Teacher

    form_class = TeacherForm

    template_name = "teacher_form.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.add_teacher"

    success_message = "Student added successfully."

    
#--------------------------------------------------------------------------------------

class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):

    model = Teacher

    form_class = TeacherForm

    template_name = "teacher_form.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.change_teacher"

    pk_url_kwarg = "id"

    def get_queryset(self):
        return Teacher.objects.all()
    

    def form_valid(self, form):

        messages.success(
            self.request,
            "Teacher updated successfully."
        )

        return super().form_valid(form)
    
#-----------------------------------------------------------------------  
class TeacherDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):

    model = Teacher

    template_name = "teacher_confirm_delete.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.delete_teacher"

    pk_url_kwarg = "id"

    def get_queryset(self):
        return Teacher.objects.all()

    def form_valid(self, form):

        messages.success(
            self.request,
            "Teacher deleted successfully."
        )

        return super().form_valid(form)
    
#---------------------------------------------------------------

class TeacherDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Teacher

    template_name = "teacher_detail.html"

    context_object_name = "teacher"

    permission_required = "teachers.view_teacher"

    pk_url_kwarg = "id"


    def get_queryset(self):

        return Teacher.objects.all()

            

        