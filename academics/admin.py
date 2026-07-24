
from django.contrib import admin
from .models import (
    Session,
    StudentClass,
    Section,
    BloodGroup,
    School,
)


admin.site.register(Session)
admin.site.register(StudentClass)
admin.site.register(Section)
admin.site.register(BloodGroup)
admin.site.register(School)