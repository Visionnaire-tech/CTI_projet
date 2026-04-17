from django.urls import path
from .views import import_students , admin_home, admin_dashboard, admin_student_detail
from deliberation.views import admin_deliberation_view
from .views import admin_courses, admin_assignments, admin_teachers, admin_ues
from academics.views import admin_deliberation_view

urlpatterns = [
    path('import-students/', import_students),
    path('', admin_home, name='admin_home'),
    path("deliberation/admin/student/<int:student_id>/", admin_student_detail, name="admin_student_detail"),

    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path("students/", admin_deliberation_view, name="admin_students"),
    #path('students/', admin_students, name='admin_students'),
    #path('student/<int:student_id>/', admin_student_detail, name='admin_student_detail'),

    path('deliberation/<int:promotion_id>/', admin_deliberation_view, name='admin_deliberation'),

    # 🔥 gestion académique
    path('courses/', admin_courses, name='admin_courses'),
    path('assignments/', admin_assignments, name='admin_assignments'),
    path('teachers/', admin_teachers, name='admin_teachers'),
    path('ues/', admin_ues, name='admin_ues'),

]