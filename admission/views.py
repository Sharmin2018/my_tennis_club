from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.mixins import SuccessMessageMixin
from .models import AdmissionApplication
from .forms import AdmissionApplicationForm
from django.views.generic import TemplateView,ListView,DetailView

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin




class AdmissionCreateView(SuccessMessageMixin, CreateView):
    model = AdmissionApplication
    form_class = AdmissionApplicationForm
    template_name = "admission/admission_form.html"
    success_url = reverse_lazy("admission_success")
    success_message = "Your admission application has been submitted successfully."

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class AdmissionListView(ListView):

    model = AdmissionApplication
    template_name = "admission/admission_list.html"
    context_object_name = "applications"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):

        queryset = AdmissionApplication.objects.select_related(
            "student_class",
            "section",
            "department",
            "admission_session",
        ).order_by("-created_at")

        search = self.request.GET.get("search")
        status = self.request.GET.get("status")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset


class AdmissionDetailView(DetailView):

    model = AdmissionApplication

    template_name = "admission/admission_detail.html"

    context_object_name = "application"



class AdmissionSuccessView(TemplateView):

    template_name = "admission/admission_success.html"


class AdmissionApproveView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "admission.change_admissionapplication"
    def get(self, request, pk):

        application = get_object_or_404(
            AdmissionApplication,
            pk=pk
        )

        if application.status == "Approved":

            messages.warning(
            request,
            "Already approved."
        )

            return redirect(
            "admission_detail",
            pk=pk,
            )

        if application.status != "Verified":

            messages.error(
            request,
            "Please verify the application first."
            )

            return redirect(
            "admission_detail",
            pk=pk,
            )

        
        application.create_student(request.user)

        messages.success(
            request,
            "Student admitted successfully."
        )

        return redirect(
            "admission_detail",
            pk=pk,
        )
    
class AdmissionRejectView( LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "admission.change_admissionapplication"

    def get(self, request, pk):

        application = get_object_or_404(
            AdmissionApplication,
            pk=pk
        )

        if application.status == "Approved":

            messages.error(
             request,
            "Approved application cannot be rejected."
            )

            return redirect(
                "admission_detail",
                pk=pk,
            )
        
        if application.status == "Rejected":

            messages.warning(
            request,
            "Application is already rejected."
            )

            return redirect(
            "admission_detail",
            pk=pk,
            )

        application.status = "Rejected"
        application.save()

        messages.success(
            request,
            "Application rejected successfully."
        )

        return redirect("admission_detail", pk=pk)
    
class AdmissionVerifyView( LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "admission.change_admissionapplication"

    def get(self, request, pk):

        application = get_object_or_404(
            AdmissionApplication,
            pk=pk
        )
        if application.status == "Verified":

            messages.warning(
            request,
            "Application is already verified."
            )

            return redirect(
            "admission_detail",
            pk=pk,
            )
        
        if application.status == "Approved":

            messages.warning(
            request,
             "Application has already been approved."
            )

            return redirect(
            "admission_detail",
             pk=pk,
            )
        if application.status != "Pending":

            messages.warning(
                request,
                "This application cannot be verified."
            )

            return redirect("admission_detail", pk=pk)
        
        if application.status == "Rejected":

            messages.warning(
            request,
            "Rejected application cannot be verified."
            )

            return redirect(
            "admission_detail",
            pk=pk,
        )


        application.status = "Verified"
        application.save()

        messages.success(
            request,
            "Application verified successfully."
        )

        return redirect("admission_list")