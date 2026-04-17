from django.contrib import admin
from .models import Grade

class GradeAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'tp',
        'interro',
        'examen',
        'note_finale',
        'statut'
    )

    list_filter = ('course',)
    search_fields = ('student__matricule',)

admin.site.register(Grade, GradeAdmin)
