from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from members.models import Student
from teachers.models import Teacher
from staffs.models import Staff
from departments.models import Department
from notices.models import Notice

# -------------------------
# Dashboard View
# -------------------------

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["student_count"] = Student.objects.count()

        context["male_students"] = Student.objects.filter(
        gender="Male"
        ).count()

        context["female_students"] = Student.objects.filter(
        gender="Female"
         ).count()

        context["photo_students"] = Student.objects.exclude(
        photo=""
        ).count()

        context["teacher_count"] = Teacher.objects.count()

        context["male_teachers"] = Teacher.objects.filter(
        gender="Male"
        ).count()

        context["female_teachers"] = Teacher.objects.filter(
        gender="Female"
         ).count()

        context["staff_count"] = Staff.objects.count()

        context["male_staffs"] = Staff.objects.filter(
        gender="Male"
        ).count()

        context["female_staffs"] = Staff.objects.filter(
        gender="Female"
         ).count()

        context["department_count"] = Department.objects.count()

        context["notice_count"] = Notice.objects.count()

        context["latest_students"] = Student.objects.order_by("-id")[:5]

        context["latest_teachers"] = Teacher.objects.order_by("-id")[:5]

        context["latest_notices"] = Notice.objects.order_by("-publish_date")[:5]

        return context
    
 