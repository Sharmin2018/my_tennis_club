from django.db.models import Q
from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Staff
from .forms import StaffForm
from core.mixins import UserCreateMixin


# ----------------------------------------------------------------------

class StaffListView(LoginRequiredMixin, ListView):

    model = Staff

    template_name = "staff_list.html"

    context_object_name = "staffs"

    paginate_by = 3

    def get_queryset(self):

        query = self.request.GET.get("q")

        queryset = Staff.objects.all()

        if query:

            queryset = queryset.filter(

                Q(name__icontains=query) |

                Q(email__icontains=query) |

                Q(phone__icontains=query) |

                Q(designation__icontains=query) |

                Q(department__name__icontains=query)

            )

        return queryset.order_by("-id")


# ----------------------------------------------------------------------

class StaffCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserCreateMixin,
    CreateView
):

    model = Staff

    form_class = StaffForm

    template_name = "staff_form.html"

    success_url = reverse_lazy("staff_list")

    permission_required = "staffs.add_staff"

    success_message = "Staff added successfully."


# ----------------------------------------------------------------------

class StaffUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):

    model = Staff

    form_class = StaffForm

    template_name = "staff_form.html"

    success_url = reverse_lazy("staff_list")

    permission_required = "staffs.change_staff"

    pk_url_kwarg = "id"

    def get_queryset(self):

        return Staff.objects.all()

    def form_valid(self, form):

        messages.success(
            self.request,
            "Staff updated successfully."
        )

        return super().form_valid(form)


# ----------------------------------------------------------------------

class StaffDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):

    model = Staff

    template_name = "staff_confirm_delete.html"

    success_url = reverse_lazy("staff_list")

    permission_required = "staffs.delete_staff"

    pk_url_kwarg = "id"

    def get_queryset(self):

        return Staff.objects.all()

    def form_valid(self, form):

        messages.success(
            self.request,
            "Staff deleted successfully."
        )

        return super().form_valid(form)


# ----------------------------------------------------------------------

class StaffDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Staff

    template_name = "staff_detail.html"

    context_object_name = "staff"

    permission_required = "staffs.view_staff"

    pk_url_kwarg = "id"

    def get_queryset(self):

        return Staff.objects.all()