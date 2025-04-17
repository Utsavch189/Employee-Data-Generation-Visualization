from django.contrib import admin
from app.models import Employee, Attendance, Performance, Salary

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Performance)
admin.site.register(Salary)