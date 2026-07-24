from django.urls import path
from . import views



urlpatterns = [
   

    path("", views.StudentListView.as_view(), name="student_list"),

    path("add/", views.StudentCreateView.as_view(), name="student_add"),

    path("edit/<int:id>/", views.StudentUpdateView.as_view(), name="student_edit"),

    path("delete/<int:id>/", views.StudentDeleteView.as_view(), name="student_delete"),
    
    path("detail/<int:id>/", views.StudentDetailView.as_view(), name="student_detail"),

    path(
    "profile/<int:pk>/print/",
    views.StudentPrintView.as_view(),
    name="student_print",
    ),




]