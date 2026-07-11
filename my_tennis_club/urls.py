from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),
    path("teachers/", include("teachers.urls")),
    path("staff/",include("staffs.urls"),),
    path("department/",include("departments.urls"),),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )