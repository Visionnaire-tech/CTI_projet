from django.contrib import admin
from .models import Section, Department, Promotion, Student, Semester, UE

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'matricule',
        'nom',
        'prenom',
        'get_section',   # ✅ correction
        'promotion',
        'is_active'
    )

    list_filter = ('promotion', 'department__section')  # ✅ filtre indirect
    search_fields = ('matricule', 'nom')

    def get_section(self, obj):
        return obj.department.section if obj.department else None

    get_section.short_description = "Section"

admin.site.register(Student, StudentAdmin)
admin.site.register(Section)
admin.site.register(Department)
admin.site.register(Promotion)
admin.site.register(Semester)
admin.site.register(UE)