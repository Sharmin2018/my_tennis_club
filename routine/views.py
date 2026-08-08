from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse

from .models import Routine
from .forms import RoutineForm


class RoutineListView(LoginRequiredMixin, ListView):

    model = Routine

    template_name = "routine/list.html"

    context_object_name = "routines"

    paginate_by = 10

    def get_queryset(self):

        queryset = Routine.objects.select_related(
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__department",
            "subject_assignment__session",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).order_by(
            "day",
            "start_time"
        )

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(

                Q(subject_assignment__subject__name__icontains=search) |

                Q(subject_assignment__teacher__name__icontains=search) |

                Q(room__icontains=search)

            )

        return queryset


class RoutineCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):

    model = Routine

    form_class = RoutineForm

    template_name = "routine/form.html"

    success_url = reverse_lazy("routine_list")

    success_message = "Routine added successfully."


class RoutineUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):

    model = Routine

    form_class = RoutineForm

    template_name = "routine/form.html"

    success_url = reverse_lazy("routine_list")

    success_message = "Routine updated successfully."


class RoutineDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Routine

    template_name = "routine/detail.html"

    context_object_name = "routine"


class RoutineDeleteView(
    LoginRequiredMixin,
    View
):

    def post(self, request, pk):

        routine = get_object_or_404(
            Routine,
            pk=pk
        )

        routine.delete()

        return JsonResponse({

            "status": "success",

            "message": "Routine deleted successfully."

        })