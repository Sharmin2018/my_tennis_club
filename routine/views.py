from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse


from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

from .models import Routine, Period
from .forms import RoutineForm



# =========================================================
# ROUTINE GRID CONSTANTS
# =========================================================

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
]


def build_routine_grid(routines):

    periods = list(
        Period.objects.filter(
            is_active=True
        ).order_by("number")
    )

    routine_map = {}

    for routine in routines:

        if routine.period_id:

            key = (
                routine.day,
                routine.period_id
            )

            routine_map[key] = routine

    grid = []

    for day in DAYS:

        row = {
            "day": day,
            "cells": []
        }

        for period in periods:

            routine = routine_map.get(
                (day, period.id)
            )

            row["cells"].append({
                "period": period,
                "routine": routine,
            })

        grid.append(row)

    return {
        "days": DAYS,
        "periods": periods,
        "grid": grid,
    }



# =========================================================
# NORMAL ROUTINE LIST
# =========================================================

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
            "period__number"
        )

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(

                Q(
                    subject_assignment__subject__name__icontains=search
                )
                |
                Q(
                    subject_assignment__subject__code__icontains=search
                )
                |
                Q(
                    subject_assignment__teacher__name__icontains=search
                )
                |
                Q(
                    room__icontains=search
                )
            )

        return queryset


# =========================================================
# ADD ROUTINE
# =========================================================

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


# =========================================================
# EDIT ROUTINE
# =========================================================

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


# =========================================================
# ROUTINE DETAIL
# =========================================================

class RoutineDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Routine

    template_name = "routine/detail.html"

    context_object_name = "routine"


# =========================================================
# AJAX DELETE
# =========================================================

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



# =========================================================
# ROUTINE CONFLICT CHECK
# =========================================================

class RoutineConflictCheckView(LoginRequiredMixin, View):

    def get(self, request):

        subject_assignment_id = request.GET.get(
            "subject_assignment"
        )

        day = request.GET.get("day")

        period_id = request.GET.get("period")

        room = request.GET.get("room")

        routine_id = request.GET.get("routine_id")

        if not all([
            subject_assignment_id,
            day,
            period_id,
            room
        ]):
            return JsonResponse({
                "conflict": False
            })

        queryset = Routine.objects.filter(
            day=day,
            period_id=period_id,
            is_active=True,
        ).select_related(
            "subject_assignment__teacher",
            "subject_assignment__student_class",
            "subject_assignment__section",
        )

        # Edit করার সময় নিজের record বাদ দিতে হবে
        if routine_id:
            queryset = queryset.exclude(
                pk=routine_id
            )

        conflicts = []

        # -------------------------------------------------
        # SECTION CONFLICT
        # -------------------------------------------------

        selected = get_object_or_404(
            Routine.objects.model._meta.get_field(
                "subject_assignment"
            ).remote_field.model,
            pk=subject_assignment_id
        )

        for routine in queryset:

            assignment = routine.subject_assignment

            # Same class + section
            if (
                assignment.student_class_id
                == selected.student_class_id
                and
                assignment.section_id
                == selected.section_id
            ):

                conflicts.append(
                    "This section already has another class "
                    "in this period."
                )

                break

        # -------------------------------------------------
        # TEACHER CONFLICT
        # -------------------------------------------------

        for routine in queryset:

            if (
                routine.subject_assignment.teacher_id
                == selected.teacher_id
            ):

                conflicts.append(
                    "This teacher already has another class "
                    "in this period."
                )

                break

        # -------------------------------------------------
        # ROOM CONFLICT
        # -------------------------------------------------

        for routine in queryset:

            if routine.room.strip().lower() == room.strip().lower():

                conflicts.append(
                    "This classroom is already occupied "
                    "in this period."
                )

                break

        return JsonResponse({

            "conflict": bool(conflicts),

            "messages": conflicts

        })

# =========================================================
# STUDENT ROUTINE
# =========================================================

class StudentRoutineView(LoginRequiredMixin, ListView):

    model = Routine

    template_name = "routine/student.html"

    context_object_name = "routines"

    def get_queryset(self):

        return Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        routines = self.get_queryset()

        context.update(
            build_routine_grid(routines)
        )

        return context

# =========================================================
# TEACHER ROUTINE
# =========================================================

class TeacherRoutineView(LoginRequiredMixin, ListView):

    model = Routine

    template_name = "routine/teacher.html"

    context_object_name = "routines"

    def get_queryset(self):

        return Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        routines = self.get_queryset()

        context.update(
            build_routine_grid(routines)
        )

        return context

# =========================================================
# CLASS ROOM ROUTINE
# =========================================================

class ClassroomRoutineView(LoginRequiredMixin, ListView):

    model = Routine

    template_name = "routine/classroom.html"

    context_object_name = "routines"

    def get_queryset(self):

        return Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        routines = self.get_queryset()

        context.update(
            build_routine_grid(routines)
        )

        return context