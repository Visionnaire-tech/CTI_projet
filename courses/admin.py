
from django.contrib import admin
from .models import Teacher, Course, CourseAssignment

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('nom', 'user')

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course)
admin.site.register(CourseAssignment)