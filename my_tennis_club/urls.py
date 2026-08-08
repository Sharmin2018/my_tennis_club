from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),
    
    path("accounts/", include("accounts.urls")),

    path("admission/",include("admission.urls"),),

    # Dashboard
    path("dashboard/", include("core.urls")),

    # Admin Modules
    path("students/", include("members.urls")),
    path("teachers/", include("teachers.urls")),
    path("staffs/", include("staffs.urls")),
    path("departments/", include("departments.urls")),
    path("notices/", include("notices.urls")),
    path("promotion/",include("promotion.urls"),),
    path("attendance/",include("attendance.urls"),),
    path("subjects/",include("subjects.urls"),),
    path("routine/",include("routine.urls"),),
    
    # Public Website
    path("", include("website.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )