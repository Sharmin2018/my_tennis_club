from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.RoutineListView.as_view(),
        name="routine_list",
    ),

    path(
        "add/",
        views.RoutineCreateView.as_view(),
        name="routine_add",
    ),

    path("<int:pk>/",views.RoutineDetailView.as_view(),name="routine_detail",),

    path("edit/<int:pk>/",views.RoutineUpdateView.as_view(),name="routine_edit",),

    path(
        "delete/<int:pk>/",
        views.RoutineDeleteView.as_view(),
        name="routine_delete",
    ),
]