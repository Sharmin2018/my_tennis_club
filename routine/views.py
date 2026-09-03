from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from academics.models import StudentClass, Session, Section
from teachers.models import Teacher
from departments.models import Department
from datetime import datetime

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

    periods = Period.objects.filter(
        is_active=True
    ).order_by("number")

    days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
    ]

    routine_map = {}

    for routine in routines:

        key = (
            routine.day,
            routine.period_id
        )

        routine_map[key] = routine

    grid = []

    for day in days:

        cells = []

        for period in periods:

            routine = routine_map.get(
                (day, period.id)
            )

            cells.append({
                "period": period,
                "routine": routine,
            })

        grid.append({
            "day": day,
            "cells": cells,
        })

    return {
        "periods": periods,
        "days": days,
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

        qs = Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__department",
            "subject_assignment__session",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

        # -----------------------------
        # GET FILTER VALUES
        # -----------------------------

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        department = self.request.GET.get("department")
        session = self.request.GET.get("session")
        student_class = self.request.GET.get("student_class")
        section = self.request.GET.get("section")

        # -----------------------------
        # FILTER
        # -----------------------------

        if month:
            qs = qs.filter(month=month)

        if year:
            qs = qs.filter(year=year)

        if department:
            qs = qs.filter(
                subject_assignment__department_id=department
            )

        if session:
            qs = qs.filter(
                subject_assignment__session_id=session
            )

        if student_class:
            qs = qs.filter(
                subject_assignment__student_class_id=student_class
            )

        if section:
            qs = qs.filter(
                subject_assignment__section_id=section
            )

        return qs.order_by(
            "day",
            "period__number"
        )

   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

    # =================================================
    # FILTER VALUES
    # =================================================

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        department_id = self.request.GET.get("department")
        session_id = self.request.GET.get("session")
        student_class_id = self.request.GET.get("student_class")
        section_id = self.request.GET.get("section")

    # =================================================
    # SELECTOR DATA
    # =================================================

        context["departments"] = Department.objects.all().order_by("name")

        context["sessions"] = Session.objects.all().order_by("name")

        context["classes"] = StudentClass.objects.all().order_by("id")

        context["sections"] = Section.objects.all().order_by("id")

    # =================================================
    # MONTHS
    # =================================================

        context["months"] = Routine._meta.get_field(
            "month"
        ).choices

    # =================================================
    # YEARS
    # =================================================

        context["years"] = range(2025, 2051)

    # =================================================
    # PERIODS
    # =================================================

        context["periods"] = Period.objects.filter(
            is_active=True
        ).order_by("number")

    # =================================================
    # SELECTED OBJECTS
    # =================================================

        selected_department = None
        selected_session = None
        selected_class = None
        selected_section = None

        if department_id:
            selected_department = Department.objects.filter(
                pk=department_id
            ).first()

        if session_id:
            selected_session = Session.objects.filter(
                pk=session_id
            ).first()

        if student_class_id:
            selected_class = StudentClass.objects.filter(
                pk=student_class_id
            ).first()

        if section_id:
            selected_section = Section.objects.filter(
                pk=section_id
            ).first()

    # =================================================
    # ROUTINES
    # =================================================

        routines = self.get_queryset()

    # =================================================
    # BUILD GRID
    # =================================================

        grid = build_routine_grid(routines)

    # =================================================
    # TOTAL PERIOD / WEEK
    # =================================================

        total_periods_week = routines.count()

    # =================================================
    # MONTH NAME
    # =================================================

        month_name = ""

        if month:

            month_choices = dict(
                Routine._meta.get_field("month").choices
            )

            month_name = month_choices.get(
                int(month),
                ""
            )

    # =================================================
    # CONTEXT
    # =================================================

        context["grid"] = grid

    # Selector selected values
        context["selected_month"] = month
        context["selected_year"] = year

        context["selected_department"] = department_id
        context["selected_session"] = session_id
        context["selected_class"] = student_class_id
        context["selected_section"] = section_id

    # Heading names
        context["selected_class_name"] = (
            str(selected_class)
            if selected_class
            else ""
        )

        context["selected_section_name"] = (
            str(selected_section)
            if selected_section
            else ""
        )

        context["department_name"] = (
            str(selected_department)
            if selected_department
            else ""
        )

        context["session_name"] = (
            str(selected_session)
            if selected_session
            else ""
        )

        context["total_periods_week"] = total_periods_week

        context["month_name"] = month_name

        context["title"] = "Student Routine"

        return context


# =========================================================
# TEACHER ROUTINE
# =========================================================

class TeacherRoutineView(LoginRequiredMixin, ListView):

    model = Routine
    template_name = "routine/teacher.html"
    context_object_name = "routines"

    def get_queryset(self):

        qs = Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__department",
            "subject_assignment__session",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        department = self.request.GET.get("department")
        session = self.request.GET.get("session")
        teacher = self.request.GET.get("teacher")

        if month:
            qs = qs.filter(month=month)

        if year:
            qs = qs.filter(year=year)

        if department:
            qs = qs.filter(
                subject_assignment__department_id=department
            )

        if session:
            qs = qs.filter(
                subject_assignment__session_id=session
            )

        if teacher:
            qs = qs.filter(
                subject_assignment__teacher_id=teacher
            )

        return qs.order_by(
            "day",
            "period__number"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        department_id = self.request.GET.get("department")
        session_id = self.request.GET.get("session")
        teacher_id = self.request.GET.get("teacher")

        # =================================================
        # SELECTOR DATA
        # =================================================

        context["departments"] = Department.objects.all().order_by("name")

        context["sessions"] = Session.objects.all().order_by("name")

        context["teachers"] = Teacher.objects.all().order_by("name")

        context["months"] = Routine._meta.get_field(
            "month"
        ).choices

        context["years"] = range(2025, 2051)

        context["periods"] = Period.objects.filter(
            is_active=True
        ).order_by("number")

        # =================================================
        # SELECTED OBJECTS
        # =================================================

        selected_department = None
        selected_session = None
        selected_teacher = None

        if department_id:

            selected_department = Department.objects.filter(
                pk=department_id
            ).first()

        if session_id:

            selected_session = Session.objects.filter(
                pk=session_id
            ).first()

        if teacher_id:

            selected_teacher = Teacher.objects.filter(
                pk=teacher_id
            ).first()

        # =================================================
        # ROUTINES
        # =================================================

        routines = self.get_queryset()

        # =================================================
        # BUILD GRID
        # =================================================

        grid = build_routine_grid(routines)

        # =================================================
        # TOTAL PERIOD / WEEK
        # =================================================

        total_periods_week = routines.count()

        # =================================================
        # MONTH NAME
        # =================================================

        month_name = ""

        if month:

            month_choices = dict(
                Routine._meta.get_field("month").choices
            )

            month_name = month_choices.get(
                int(month),
                ""
            )

        # =================================================
        # CONTEXT
        # =================================================

        context["grid"] = grid

        context["selected_month"] = month
        context["selected_year"] = year

        context["selected_department"] = department_id
        context["selected_session"] = session_id
        context["selected_teacher"] = teacher_id
       

        context["department_name"] = (
            str(selected_department)
            if selected_department
            else ""
        )

        context["session_name"] = (
            str(selected_session)
            if selected_session
            else ""
        )

        context["teacher_name"] = (
            str(selected_teacher)
            if selected_teacher
            else ""
        )
        context["selected_teacher_name"] = (
                            selected_teacher.name
                            if selected_teacher
                            else ""
                            )
        context["selected_teacher_designation"] = (
                    selected_teacher.designation
                    if selected_teacher
                    else ""
                    )

        context["total_periods_week"] = total_periods_week

        context["month_name"] = month_name

        context["title"] = "Teacher Routine"

        return context



# =========================================================
# CLASSROOM ROUTINE
# =========================================================

class ClassroomRoutineView(LoginRequiredMixin, ListView):

    model = Routine
    template_name = "routine/classroom.html"
    context_object_name = "routines"

    def get_queryset(self):

        qs = Routine.objects.select_related(
            "period",
            "subject_assignment",
            "subject_assignment__subject",
            "subject_assignment__teacher",
            "subject_assignment__department",
            "subject_assignment__session",
            "subject_assignment__student_class",
            "subject_assignment__section",
        ).filter(
            is_active=True
        )

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        room = self.request.GET.get("room")

        if month:

            qs = qs.filter(
                month=month
            )

        if year:

            qs = qs.filter(
                year=year
            )

        if room:

            qs = qs.filter(
                room__iexact=room.strip()
            )

        return qs.order_by(
            "day",
            "period__number"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        room = self.request.GET.get("room")

        # =================================================
        # MONTH
        # =================================================

        context["months"] = Routine._meta.get_field(
            "month"
        ).choices

        # =================================================
        # YEAR
        # =================================================

        context["years"] = range(2025, 2031)

        # =================================================
        # PERIODS
        # =================================================

        context["periods"] = Period.objects.filter(
            is_active=True
        ).order_by("number")

        # =================================================
        # ROOM LIST
        # =================================================

        rooms = (
            Routine.objects
            .filter(is_active=True)
            .values_list("room", flat=True)
            .distinct()
            .order_by("room")
        )

        context["rooms"] = rooms

        # =================================================
        # ROUTINES
        # =================================================

        routines = self.get_queryset()

        # =================================================
        # BUILD GRID
        # =================================================

        grid = build_routine_grid(routines)

        # =================================================
        # TOTAL PERIOD / WEEK
        # =================================================

        total_periods_week = routines.count()

        # =================================================
        # MONTH NAME
        # =================================================

        month_name = ""

        if month:

            month_choices = dict(
                Routine._meta.get_field("month").choices
            )

            month_name = month_choices.get(
                int(month),
                ""
            )

        # =================================================
        # CONTEXT
        # =================================================

        context["grid"] = grid

        context["selected_month"] = month
        context["selected_year"] = year

        context["selected_room"] = room

        context["room_name"] = room or ""

        context["total_periods_week"] = total_periods_week

        context["month_name"] = month_name

        context["title"] = "Classroom Routine"

        return context