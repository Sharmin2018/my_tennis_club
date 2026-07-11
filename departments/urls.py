from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.DepartmentListView.as_view(),
        name="department_list",
    ),

    path(
        "add/",
        views.DepartmentCreateView.as_view(),
        name="department_add",
    ),

    path(
        "edit/<int:id>/",
        views.DepartmentUpdateView.as_view(),
        name="department_edit",
    ),

    path(
        "delete/<int:id>/",
        views.DepartmentDeleteView.as_view(),
        name="department_delete",
    ),

    path(
        "detail/<int:id>/",
        views.DepartmentDetailView.as_view(),
        name="department_detail",
    ),

]