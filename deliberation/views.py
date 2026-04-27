from django.shortcuts import render, redirect
from academics.models import Student, UE
from evaluations.models import Grade
from .services import calcul_deliberation
from django.shortcuts import render
from academics.models import Student, UE, Promotion
from evaluations.models import Grade
from django.contrib.auth import logout
from django.http import HttpResponse
from .excel import export_deliberation_excel
from accounts.views import login_view
from django.shortcuts import get_object_or_404
from courses.models import Course

from .pdf import generate_student_pdf
import os
from django.forms import modelformset_factory

def edit_student_grades(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    courses = Course.objects.filter(
        promotion=student.promotion
    ).select_related('ue')

    grades = {
        g.course_id: g
        for g in Grade.objects.filter(student=student)
    }

    if request.method == "POST":

        for course in courses:

            tp = request.POST.get(f"tp_{course.id}")
            interro = request.POST.get(f"interro_{course.id}")
            examen = request.POST.get(f"examen_{course.id}")
            statut = request.POST.get(f"statut_{course.id}")

            grade = grades.get(course.id)

            if not grade:
                grade = Grade(student=student, course=course)

            #  conversion sécurisée
            grade.tp = float(tp) if tp else None
            grade.interro = float(interro) if interro else None
            grade.examen = float(examen) if examen else None
            grade.statut = statut if statut else 'normal'

            grade.save(bypass_lock=True)  # ici ça calcule note_finale automatiquement

        return redirect('admin_student_detail', student_id=student.id)

    context = {
        'student': student,
        'courses': courses,
        'grades': grades
    }

    return render(request, 'deliberation/admin/edit_grades.html', context)

def student_pdf_view(request, student_id):
    student = Student.objects.get(id=student_id)

    file_path = f"bulletin_{student.id}.pdf"

    generate_student_pdf(student, file_path)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="bulletin_{student.id}.pdf"'
        return response

def export_excel_view(request, promotion_id):

    return export_deliberation_excel(request, promotion_id)


def admin_deliberation_view(request):

    # =======================
    # FILTRES GET
    # =======================
    promotion_id = request.GET.get("promotion")
    department_id = request.GET.get("department")
    section_id = request.GET.get("section")

    students = Student.objects.all()

    # =======================
    # PROMOTION (FIX IMPORTANT)
    # =======================
    promotion = None
    if promotion_id:
        promotion = Promotion.objects.filter(id=promotion_id).first()
        students = students.filter(promotion_id=promotion_id)

    if department_id:
        students = students.filter(department_id=department_id)

    if section_id:
        students = students.filter(department__section_id=section_id)

    # =======================
    # UE + COURS
    # =======================
    ues = UE.objects.all().prefetch_related('course_set')

    results = []

    # =======================
    # CALCUL DÉLIBÉRATION
    # =======================
    for student in students:

        total_tnp = 0
        total_credit = 0
        ue_data = []

        for ue in ues:

            courses = ue.course_set.all()

            ue_tnp = 0
            ue_credit = 0
            courses_data = []

            for course in courses:

                grade = Grade.objects.filter(
                    student=student,
                    course=course
                ).first()

                note = grade.note_finale if grade and grade.note_finale else 0
                credit = course.credit
                tnp = note * credit

                ue_tnp += tnp
                ue_credit += credit

                courses_data.append({
                    'course': course,
                    'note': note,
                    'credit': course.credit,
                    'tnp': tnp,
                    'is_zero': note < 10,
                    'grade_id': grade.id if grade else None
                })

            moyenne_ue = ue_tnp / ue_credit if ue_credit else 0

            total_tnp += ue_tnp
            total_credit += ue_credit

            ue_data.append({
                "ue": ue,
                "courses": courses_data,
                "moyenne": round(moyenne_ue, 2)
            })

        moyenne_generale = total_tnp / total_credit if total_credit else 0

        decision = (
            "ADM" if moyenne_generale >= 10
            else "AJ" if moyenne_generale >= 8
            else "DEF"
        )

        results.append({
            "student": student,
            "ues": ue_data,
            "moyenne": round(moyenne_generale, 2),
            "decision": decision
        })

    # =======================
    # RENDER FINAL
    # =======================
    return render(request, "deliberation/admin_table.html", {
        "results": results,
        "promotion": promotion
    })

def student_login(request):
    if request.method == "POST":
        matricule = request.POST.get("matricule")

        try:
            student = Student.objects.get(matricule=matricule)
            request.session['student_id'] = student.id
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            return render(request, 'deliberation/student_login.html', {
                'error': 'Matricule incorrect'
            })

    return render(request, 'deliberation/student_login.html')


def student_dashboard(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)

    return render(request, 'deliberation/student_dashboard.html', {
        'student': student
    })

def student_result(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)

    result = calcul_deliberation(student)

    return render(request, "deliberation/student_result.html", {
        "student": student,
        "ues": result['ues'],
        "moyenne": result['moyenne'],
        "credits": result['credits'],
        "decision": result['decision']
    })


def custom_logout(request):
    # 🔴 Déconnexion Django (enseignant/admin)
    logout(request)

    # 🔴 Suppression session étudiant
    if 'student_id' in request.session:
        del request.session['student_id']

    return redirect('student_login')  
    # ou 'home'

    if request.user.is_authenticated:
        logout(request)
    return redirect('login_view')
