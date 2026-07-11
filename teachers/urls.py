from django.urls import path
from . import views

urlpatterns = [
    path("", views.TeacherListView.as_view(), name="teacher_list"),

    path("add/", views.TeacherCreateView.as_view(), name="teacher_add"),

    path("edit/<int:id>/", views.TeacherUpdateView.as_view(), name="teacher_edit"),

    path("delete/<int:id>/",views.TeacherDeleteView.as_view(),name="teacher_delete"),

    path("detail/<int:id>/", views.TeacherDetailView.as_view(),name="teacher_detail"),
]