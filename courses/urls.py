from django.urls import path
from evaluations.views import saisir_notes
from .views import teacher_courses , erreur

urlpatterns = [
    path("mes-cours/", teacher_courses, name="teacher_courses"),
    path("saisir/<int:assignment_id>/", saisir_notes, name="saisir_notes"),
    path("erreur/", erreur, name="erreur"),
]