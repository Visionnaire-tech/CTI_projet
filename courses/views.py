from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CourseAssignment, Teacher


@login_required
def teacher_courses(request):

    teacher = getattr(request.user, "teacher", None)

    if teacher is None:
        return render(request, "courses/erreur.html", {
            "message": "Aucun professeur associé à ce compte."
        })

    cours = teacher.courseassignment_set.all()

    return render(request, "courses/mes_cours.html", {
        "assignments": cours
    })

def erreur(request, message):
    return render(request, "courses/erreur.html", {
        "message": message
    })