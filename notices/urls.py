from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.NoticeListView.as_view(),
        name="notice_list",
    ),

    path(
        "add/",
        views.NoticeCreateView.as_view(),
        name="notice_add",
    ),

    path(
        "detail/<int:id>/",
        views.NoticeDetailView.as_view(),
        name="notice_detail",
    ),

    path(
        "edit/<int:id>/",
        views.NoticeUpdateView.as_view(),
        name="notice_edit",
    ),

    path(
        "delete/<int:id>/",
        views.NoticeDeleteView.as_view(),
        name="notice_delete",
    ),

]