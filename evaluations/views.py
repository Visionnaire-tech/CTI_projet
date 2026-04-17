from django.shortcuts import render, get_object_or_404, redirect
from academics.models import Student, Promotion, Department
from django.contrib.auth.decorators import login_required
from courses.models import Course ,CourseAssignment
from .models import Grade
from django.core.mail import send_mail
from django.contrib import messages

@login_required
def saisir_notes(request, assignment_id):
    assignment = get_object_or_404(CourseAssignment, id=assignment_id)
    course = assignment.course

    students = Student.objects.filter(
        promotion=course.promotion,
        department=assignment.department
    )

    # 🔒 CHECK SI DEJA VALIDÉ
    already_submitted = Grade.objects.filter(
        course=course,
        is_submitted=True
    ).exists()

    if already_submitted and not request.user.is_superuser:
        messages.error(request, "⚠️ Notes déjà envoyées. Modification bloquée.")
        return redirect('mes_cours')

    if request.method == "POST":

        # 🔥 bouton envoyer
        action = request.POST.get("action")

        for student in students:
            tp = request.POST.get(f"tp_{student.id}")
            interro = request.POST.get(f"interro_{student.id}")
            examen = request.POST.get(f"examen_{student.id}")
            statut = request.POST.get(f"statut_{student.id}")

            grade, created = Grade.objects.get_or_create(
                student=student,
                course=course
            )

            grade.tp = float(tp) if tp else None
            grade.interro = float(interro) if interro else None
            grade.examen = float(examen) if examen else None
            grade.statut = statut

            grade.calculer_note()

            # 🔒 SI ENVOI FINAL
            if action == "submit":
                grade.is_submitted = True

            grade.save()

# après submit
            if action == "submit":
                grade.is_submitted = True

                teacher_email = request.user.email

                notify_teacher(
                    "Notes envoyées",
                    f"Vous avez validé les notes du cours {course.name}",
                    teacher_email
                )

        return redirect('teacher_courses')

    return render(request, 'evaluations/saisir_notes.html', {
        'course': course,
        'students': students,
        'already_submitted': already_submitted
    })


def admin_notes(request):
    promotions = Promotion.objects.all()
    departments = Department.objects.all()

    students = None
    courses = None
    data = []

    promo_id = request.GET.get('promotion')
    dept_id = request.GET.get('department')

    if promo_id and dept_id:
        students = Student.objects.filter(
            promotion_id=promo_id,
            department_id=dept_id
        )

        courses = Course.objects.filter(
            promotion_id=promo_id
        )

        for student in students:
            row = {
                'student': student,
                'notes': [],
                'moyenne': 0
            }

            total = 0
            coeff = 0

            for course in courses:
                try:
                    grade = Grade.objects.get(student=student, course=course)
                    note = grade.note_finale
                except Grade.DoesNotExist:
                    note = None

                row['notes'].append(note)

                if note is not None:
                    total += note * course.credit
                    coeff += course.credit

            row['moyenne'] = round(total / coeff, 2) if coeff else 0

            data.append(row)

    return render(request, 'evaluations/admin_notes.html', {
        'promotions': promotions,
        'departments': departments,
        'data': data,
        'courses': courses
    })
    
def home(request):
    return render(request, 'home.html')