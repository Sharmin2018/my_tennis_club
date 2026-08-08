from django.views.generic import FormView,ListView

from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from .forms import AttendanceForm

from members.models import Student

from django.contrib import messages
from django.db import transaction
from .models import Attendance

from academics.models import StudentClass, Section,Session 
from departments.models import Department
from .forms import MonthlyReportForm
import calendar











class AttendanceView(FormView):

    template_name = "attendance/take_attendance.html"

    form_class = AttendanceForm

    success_url = reverse_lazy("attendance")


    def form_valid(self, form):

        session = form.cleaned_data["session"]
        student_class = form.cleaned_data["student_class"]
        section = form.cleaned_data["section"]
        department = form.cleaned_data["department"]
        date = form.cleaned_data["date"]

        students = Student.objects.filter(
            session=session,
            student_class=student_class,
            section=section,
            department=department,
        ).order_by("roll")

        attendance_dict = {}

        for attendance in Attendance.objects.filter(
            student__in=students,
            date=date,
        ):
            attendance_dict[attendance.student_id] = attendance.status

        for student in students:
            student.attendance_status = attendance_dict.get(
                student.id,
                "Present"
            )

        return render(
            self.request,
            "attendance/take_attendance.html",
            {
                "form": form,
                "students": students,
                "date": date,
            },
        )

    def post(self, request, *args, **kwargs):

        if "save_attendance" in request.POST:

            return self.save_attendance(request)

        return super().post(request, *args, **kwargs)

    def save_attendance(self, request):

        date = request.POST.get("date")

        session = request.POST.get("session")
        student_class = request.POST.get("student_class")
        section = request.POST.get("section")
        department = request.POST.get("department")

        students = Student.objects.filter(
            session_id=session,
            student_class_id=student_class,
            section_id=section,
            department_id=department,
        ).order_by("roll")

        count = 0

        with transaction.atomic():

            for student in students:

                status = request.POST.get(
                    f"status_{student.id}"
                )

                if not status:
                    continue

                Attendance.objects.update_or_create(

                    student=student,

                    date=date,

                    defaults={
                        "status": status,
                        "taken_by": request.user,
                    },
                )

                count += 1

        messages.success(
            request,
            f"{count} student's attendance saved successfully."
        )

        return redirect("attendance")

class AttendanceHistoryView(ListView):

    model = Attendance

    template_name = "attendance/history.html"

    context_object_name = "attendances"

    paginate_by = 20

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "student",
            "student__department",
            "taken_by",
        ).order_by("-date", "student__roll")

        date = self.request.GET.get("date")
        session = self.request.GET.get("session")
        student_class = self.request.GET.get("class")
        section = self.request.GET.get("section")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")

        if date:
            queryset = queryset.filter(date=date)

        if session:
            queryset = queryset.filter(student__session_id=session)

        if student_class:
            queryset = queryset.filter(student__student_class=student_class)

        if section:
            queryset = queryset.filter(student__section=section)

        if department:
            queryset = queryset.filter(student__department_id=department)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        context["sessions"] = Session.objects.all().order_by("-id")

        context["departments"] = Department.objects.all()

        context["class_list"] = StudentClass.objects.all()
        context["section_list"] = Section.objects.all()
        context["status_choices"] = Attendance.STATUS_CHOICES

  

        context["total"] = queryset.count()

        context["present"] = queryset.filter(
        status="Present"
        ).count()

        context["absent"] = queryset.filter(
            status="Absent"
        ).count()

        context["late"] = queryset.filter(
            status="Late"
        ).count()

        context["leave"] = queryset.filter(
            status="Leave"
        ).count()

        return context

class AttendancePrintView(ListView):

    model = Attendance

    template_name = "attendance/print_history.html"

    context_object_name = "attendances"

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "student",
            "student__student_class",
            "student__section",
            "student__department",
            "taken_by",
        )

        date = self.request.GET.get("date")
        session = self.request.GET.get("session")
        student_class = self.request.GET.get("class")
        section = self.request.GET.get("section")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")

        if date:
            queryset = queryset.filter(date=date)

        if session:
            queryset = queryset.filter(student__session_id=session)

        if student_class:
            queryset = queryset.filter(student__student_class_id=student_class)

        if section:
            queryset = queryset.filter(student__section_id=section)

        if department:
            queryset = queryset.filter(student__department_id=department)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by(
            "-date",
            "student__roll",
        )


class MonthlyAttendanceReportView(FormView):

    template_name = "attendance/monthly_report.html"

    form_class = MonthlyReportForm

    def form_valid(self, form):

       

        session = form.cleaned_data["session"]
        student_class = form.cleaned_data["student_class"]
        section = form.cleaned_data["section"]
        department = form.cleaned_data["department"]

        year = int(form.cleaned_data["year"])

        month_no = int(form.cleaned_data["month"])

        month_name = calendar.month_name[month_no]

        students = Student.objects.filter(
            session=session,
            student_class=student_class,
            section=section,
            department=department,
        ).order_by("roll")

        report = []

       
        working_days = (
            Attendance.objects.filter(
                date__year=year,
                date__month=month_no,
                student__session=session,
                student__student_class=student_class,
                student__section=section,
                student__department=department,
            )
            .values("date")
            .distinct()
            .count()
        )

        for student in students:

            monthly_attendance = Attendance.objects.filter(
            student=student,
            date__year=year,
            date__month=month_no,
            )

            present = monthly_attendance.filter(
                status="Present"
            ).count()

            absent = monthly_attendance.filter(
                status="Absent"
            ).count()

            late = monthly_attendance.filter(
                status="Late"
            ).count()

            leave = monthly_attendance.filter(
                status="Leave"
            ).count()

            total_attendance = (
                present +
                absent +
                late +
                leave
            )

            if working_days:
                attendance_percent = round(
                ((present + late + leave) / working_days) * 100,
                2,
            )
            else:
                attendance_percent = 0

            report.append({

                "student": student,

                "present": present,

                "absent": absent,

                "late": late,

                "leave": leave,

                "total": total_attendance,

                "attendance_percent": attendance_percent,

                })
            return render(
                self.request,
                self.template_name,
                 {
                    "form": form,
                    "report": report,
                    "working_days": working_days,
                    "month_name": month_name,
                    "year": year,
                    "session": session,
                    "student_class": student_class,
                    "section": section,
                    "department": department,
                    "attendance_percent": attendance_percent,
                },
                )