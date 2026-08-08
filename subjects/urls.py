from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.SubjectListView.as_view(),
        name="subject_list",
    ),

    path(
        "add/",
        views.SubjectCreateView.as_view(),
        name="subject_add",
    ),

    path(
        "edit/<int:id>/",
        views.SubjectUpdateView.as_view(),
        name="subject_edit",
    ),

  
    path(
    "delete/<int:pk>/",
    views.SubjectDeleteView.as_view(),
    name="subject_delete",
),

    path(
        "detail/<int:id>/",
        views.SubjectDetailView.as_view(),
        name="subject_detail",
    ),
path(
    "assignment/",
    views.SubjectAssignmentListView.as_view(),
    name="subject_assignment_list",
),

path(
    "assignment/add/",
    views.SubjectAssignmentCreateView.as_view(),
    name="subject_assignment_add",
),

path(
    "assignment/<int:pk>/",
    views.SubjectAssignmentDetailView.as_view(),
    name="subject_assignment_detail",
),

path(
    "assignment/edit/<int:pk>/",
    views.SubjectAssignmentUpdateView.as_view(),
    name="subject_assignment_edit",
),

path(
    "assignment/delete/<int:pk>/",
    views.SubjectAssignmentDeleteView.as_view(),
    name="subject_assignment_delete",
),

]