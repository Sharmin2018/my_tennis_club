from django.db.models import Q
from django.views.generic import ListView
from .models import Teacher
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import TeacherForm
from core.mixins import UserCreateMixin,SuccessMessageMixin,BaseListMixin


class TeacherListView(LoginRequiredMixin,BaseListMixin,ListView):

    model = Teacher

    template_name = "teacher_list.html"

    context_object_name = "teachers"

   

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

        return queryset.order_by(*self.ordering)

#----------------------------------------------------------------------------------

class TeacherCreateView( 
    LoginRequiredMixin,
    PermissionRequiredMixin, 
    UserCreateMixin,
    SuccessMessageMixin,
    CreateView):

    model = Teacher

    form_class = TeacherForm

    template_name = "teacher_form.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.add_teacher"

    success_message = "Teacher added successfully."

    
#--------------------------------------------------------------------------------------

class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, UpdateView):

    model = Teacher

    form_class = TeacherForm

    template_name = "teacher_form.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.change_teacher"

    pk_url_kwarg = "id"
    success_message = "Teacher updated successfully."

    def get_queryset(self):
        return Teacher.objects.all()
    

  
    
#-----------------------------------------------------------------------  
class TeacherDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):

    model = Teacher

    template_name = "teacher_confirm_delete.html"

    success_url = reverse_lazy("teacher_list")

    permission_required = "teachers.delete_teacher"

    pk_url_kwarg = "id"

    success_message = "Teacher Delated successfully."

    def get_queryset(self):
        return Teacher.objects.all()

    
    
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

            

        