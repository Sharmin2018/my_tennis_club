from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from academics.models import StudentClass
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.http import JsonResponse

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
   
    DetailView,
)

from .models import SubjectAssignment
from .forms import SubjectAssignmentForm



from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Subject
from .forms import SubjectForm


class SubjectListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = Subject
    template_name = "subjects/list.html"
    context_object_name = "subjects"
    paginate_by = 10
    permission_required = "subjects.view_subject"

    def get_queryset(self):

        queryset = Subject.objects.select_related(
            "student_class"
        ).order_by(
            "student_class__name",
            "name",
        )

        q = self.request.GET.get("q")

        student_class = self.request.GET.get("class")

        if q:
            queryset = queryset.filter(
                name__icontains=q
            )

        if student_class:
            queryset = queryset.filter(
                student_class_id=student_class
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["class_list"] = StudentClass.objects.all()

        return context


class SubjectCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):

    model = Subject

    form_class = SubjectForm

    template_name = "subjects/form.html"

    success_url = reverse_lazy("subject_list")

    permission_required = "subjects.add_subject"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Subject added successfully."
        )

        return super().form_valid(form)


class SubjectUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):

    model = Subject

    form_class = SubjectForm

    template_name = "subjects/form.html"

    pk_url_kwarg = "id"

    success_url = reverse_lazy("subject_list")

    permission_required = "subjects.change_subject"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Subject updated successfully."
        )

        return super().form_valid(form)


class SubjectDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
):

    permission_required = "subjects.delete_subject"

    def post(self, request, pk):

        subject = get_object_or_404(
            Subject,
            pk=pk
        )

        name = subject.name

        subject.delete()

        return JsonResponse({
            "success": True,
            "message": f"{name} deleted successfully."
        })


class SubjectDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):

    model = Subject

    template_name = "subjects/detail.html"

    context_object_name = "subject"

    pk_url_kwarg = "id"

    permission_required = "subjects.view_subject"


class SubjectAssignmentListView(ListView):

    model = SubjectAssignment

    template_name = "subjects/assignment_list.html"

    context_object_name = "assignments"

    paginate_by = 10


class SubjectAssignmentCreateView(
    SuccessMessageMixin,
    CreateView
):

    model = SubjectAssignment

    form_class = SubjectAssignmentForm

    template_name = "subjects/assignment_form.html"

    success_url = reverse_lazy("subject_assignment_list")

    success_message = "Subject assigned successfully."


class SubjectAssignmentUpdateView(
    SuccessMessageMixin,
    UpdateView
):

    model = SubjectAssignment

    form_class = SubjectAssignmentForm

    template_name = "subjects/assignment_form.html"

    success_url = reverse_lazy("subject_assignment_list")

    success_message = "Assignment updated successfully."


class SubjectAssignmentDetailView(
    DetailView
):

    model = SubjectAssignment

    template_name = "subjects/assignment_detail.html"


class SubjectAssignmentDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        assignment = get_object_or_404(SubjectAssignment, pk=pk)
        assignment.delete()

        return JsonResponse({
            "status": "success",
            "message": "Subject Assignment deleted successfully."
        })