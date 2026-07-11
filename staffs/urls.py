from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.StaffListView.as_view(),
        name="staff_list",
    ),

    path(
        "add/",
        views.StaffCreateView.as_view(),
        name="staff_add",
    ),

    path(
        "edit/<int:id>/",
        views.StaffUpdateView.as_view(),
        name="staff_edit",
    ),

    path(
        "delete/<int:id>/",
        views.StaffDeleteView.as_view(),
        name="staff_delete",
    ),

    path(
        "detail/<int:id>/",
        views.StaffDetailView.as_view(),
        name="staff_detail",
    ),

]