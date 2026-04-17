from django.urls import path
from .views import saisir_notes, admin_notes, home

urlpatterns = [
    path('admin-notes/', admin_notes),
    # Correct
    path('saisir/<int:assignment_id>/', saisir_notes, name='saisir_notes'),
    #path('mes-cours/', teacher_courses, name='teacher_courses'),
    path('',home, name='home'),
]