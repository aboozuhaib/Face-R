from django.contrib import admin
from .models import Attendance
from .models import StudentList

# Register your models here.

admin.site.register(Attendance)
admin.site.register(StudentList)