from django.urls import path
from . import views




urlpatterns = [

   

    path(
        "success/",
        views.AdmissionSuccessView.as_view(),
        name="admission_success",
    ),

     path(
        "list/",
        views.AdmissionListView.as_view(),
        name="admission_list",
    ),

    path(
        "detail/<int:pk>/",
        views.AdmissionDetailView.as_view(),
        name="admission_detail",
    ),

    path(
        "apply/",
        views.AdmissionCreateView.as_view(),
        name="admission_apply",
        ),
     path(
        "verify/<int:pk>/",
        views.AdmissionVerifyView.as_view(),
        name="admission_verify",
    ),

     path(
        "approve/<int:pk>/",
        views.AdmissionApproveView.as_view(),
        name="admission_approve",
    ),

        path(
        "reject/<int:pk>/",
        views.AdmissionRejectView.as_view(),
        name="admission_reject",
    ),
  
]