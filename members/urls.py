from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.student_list, name='list'),
    path('add/', views.add_student, name='add'),
    path('edit/<int:id>/', views.edit_student, name='edit'),
    path('delete/<int:id>/', views.delete_student, name='delete'),

    path('register/', views.register, name='register'),

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
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout',
    ),
]