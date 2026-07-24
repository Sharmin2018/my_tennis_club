from django.views.generic import FormView,ListView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import PromotionForm
from members.models import Student
from .models import PromotionHistory
from django.db import transaction




class PromotionView(FormView):

    template_name = "promotion/promote.html"

    form_class = PromotionForm

    success_url = reverse_lazy("promotion")

    def form_valid(self, form):

        from_class = form.cleaned_data["from_class"]
        from_section = form.cleaned_data["from_section"]
        to_class = form.cleaned_data["to_class"]

        if from_class == to_class:

            messages.error(
                self.request,
                "From Class and To Class cannot be same."
            )

            return self.form_invalid(form)

        students = Student.objects.filter(
            student_class=from_class,
            section=from_section,
            ).order_by("roll")


        if not students.exists():

            messages.warning(
            self.request,
            "No students found for this class and section."
            )

            return self.form_invalid(form)

        if "preview" in self.request.POST:

            return render(
                self.request,
                "promotion/promote.html",
                {
                    "form": form,
                    "students": students,
                    "to_class": to_class,
                },
            )

        count = 0

        with transaction.atomic():

            for student in students:

                existing = PromotionHistory.objects.filter(
                    student=student,
                    to_class=to_class,
                ).exists()

                if existing:
                    continue

                PromotionHistory.objects.create(
                    student=student,
                    from_class=student.student_class,
                    to_class=to_class,
                    section=student.section,
                    promoted_by=self.request.user,
                )

                student.student_class = to_class
                student.save()

                count += 1

        messages.success(
            self.request,
            f"{count} students promoted successfully."
        )

        return super().form_valid(form)


class PromotionHistoryView(ListView):

    model = PromotionHistory

    template_name = "promotion/history.html"

    context_object_name = "histories"

    paginate_by = 20

    ordering = ["-promoted_at"]

    def get_queryset(self):

        return PromotionHistory.objects.select_related(
            "student",
            "from_class",
            "to_class",
            "section",
            "promoted_by",
        )