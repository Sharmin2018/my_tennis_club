from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from .views import (
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    RegisterView,
    StudentDetailView,
)

urlpatterns = [
    path('', StudentListView.as_view(), name='list'),

    path('add/', StudentCreateView.as_view(), name='add'),

    path('edit/<int:id>/', StudentUpdateView.as_view(), name='edit'),

    path('delete/<int:id>/', StudentDeleteView.as_view(), name='delete'),

    path('register/', RegisterView.as_view(), name='register'),
    
    path("student/<int:id>/",StudentDetailView.as_view(),name="student_detail",),

    path("dashboard/",views.DashboardView.as_view(),name="dashboard",),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='login'
        ),
        name='logout',
    ),
]