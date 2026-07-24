from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Notice
from .forms import NoticeForm

from django.contrib import messages

from core.mixins import (
    UserCreateMixin,
    SuccessMessageMixin,
    BaseListMixin,
)


# ---------------------------------------------------------

class NoticeListView(
    LoginRequiredMixin,
    BaseListMixin,
    ListView,
):

    model = Notice

    template_name = "notice_list.html"

    context_object_name = "notices"

    paginate_by = 5

    def get_queryset(self):

        query = self.request.GET.get("q")

        queryset = Notice.objects.all()

        if query:

            queryset = queryset.filter(

                Q(title__icontains=query) |

                Q(description__icontains=query)

            )

        return queryset.order_by(*self.ordering)


# ---------------------------------------------------------

class NoticeCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserCreateMixin,
    SuccessMessageMixin,
    CreateView,
):

    model = Notice

    form_class = NoticeForm

    template_name = "notice_add.html"

    success_url = reverse_lazy("notice_list")

    permission_required = "notices.add_notice"

    success_message = "Notice added successfully."


# ---------------------------------------------------------

class NoticeUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):

    model = Notice

    form_class = NoticeForm

    template_name = "notice_add.html"

    success_url = reverse_lazy("notice_list")

    permission_required = "notices.change_notice"

    pk_url_kwarg = "id"

    success_message = "Notice updated successfully."


# ---------------------------------------------------------

class NoticeDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):

    model = Notice

    template_name = "notice_confirm_delete.html"

    success_url = reverse_lazy("notice_list")

    permission_required = "notices.delete_notice"

    pk_url_kwarg = "id"

    success_message = "Notice deleted successfully."


# ---------------------------------------------------------

class NoticeDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):

    model = Notice

    template_name = "notice_detail.html"

    context_object_name = "notice"

    permission_required = "notices.view_notice"

    pk_url_kwarg = "id"