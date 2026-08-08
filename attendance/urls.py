from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.AttendanceView.as_view(),
        name="attendance",
    ),

    path("history/",views.AttendanceHistoryView.as_view(), name="attendance_history",),

    path(
    "print/",
    views.AttendancePrintView.as_view(),
    name="attendance_print",
  ),

    path(
    "monthly-report/",
    views.MonthlyAttendanceReportView.as_view(),
    name="monthly_attendance_report",
  ),

]