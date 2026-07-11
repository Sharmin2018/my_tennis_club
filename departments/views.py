from django.db.models import Q
from core.mixins import UserCreateMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

from .models import Department
from .forms import DepartmentForm


class DepartmentListView(LoginRequiredMixin, ListView):

    model = Department

    template_name = "department_list.html"

    context_object_name = "departments"

    paginate_by = 5

    def get_queryset(self):

        query = self.request.GET.get("q")

        queryset = Department.objects.all()

        if query:

            queryset = queryset.filter(

                Q(name__icontains=query) |

                Q(department_code__icontains=query)

            )

        return queryset.order_by("name")


# ------------------------------------------------------------

class DepartmentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserCreateMixin,
    CreateView
):

    model = Department

    form_class = DepartmentForm

    template_name = "department_form.html"

    success_url = reverse_lazy("department_list")

    permission_required = "departments.add_department"

    success_message = "Department added successfully."

# ------------------------------------------------------------

class DepartmentUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):

    model = Department

    form_class = DepartmentForm

    template_name = "department_form.html"

    success_url = reverse_lazy("department_list")

    permission_required = "departments.change_department"

    pk_url_kwarg = "id"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Department updated successfully."
        )

        return super().form_valid(form)


# ------------------------------------------------------------

class DepartmentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):

    model = Department

    template_name = "department_confirm_delete.html"

    success_url = reverse_lazy("department_list")

    permission_required = "departments.delete_department"

    pk_url_kwarg = "id"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Department deleted successfully."
        )

        return super().form_valid(form)


# ------------------------------------------------------------

class DepartmentDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Department

    template_name = "department_detail.html"

    context_object_name = "department"

    permission_required = "departments.view_department"

    pk_url_kwarg = "id"