from django.urls import path
from evaluations.views import saisir_notes, import_notes_excel
from .views import teacher_courses , erreur

urlpatterns = [
    path("mes-cours/", teacher_courses, name="teacher_courses"),
    path("saisir/<int:assignment_id>/", saisir_notes, name="saisir_notes"),
    path("erreur/", erreur, name="erreur"),
    path("import-notes/<int:assignment_id>/", import_notes_excel, name="import_notes_excel"),
]