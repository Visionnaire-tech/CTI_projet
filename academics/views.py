import pandas as pd
from django.shortcuts import render
from .models import Student, Promotion, Department, Section, UE
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from courses.models import Teacher, Course
from deliberation.views import student_result
from evaluations.models import Grade
from deliberation.services import calcul_deliberation


def normalize(col):
    return col.strip().lower()


def import_students(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            return render(request, 'academics/import_students.html', {
                "error": "Aucun fichier envoyé"
            })

        df = pd.read_excel(file)
        df.columns = [normalize(c) for c in df.columns]

        created = 0

        for _, row in df.iterrows():

            matricule = str(row.get('matricule') or '').strip()
            nom = str(row.get('nom') or '').strip()
            postnom = str(row.get('postnom') or '').strip()
            prenom = str(row.get('prenom') or '').strip()

            promo_name = str(row.get('promotion') or '').strip()
            dept_name = str(row.get('department') or '').strip()
            section_name = str(row.get('section') or '').strip()

            if not matricule or not promo_name:
                continue

            try:
                section = Section.objects.get(name__iexact=section_name)
                department = Department.objects.get(name__iexact=dept_name, section=section)
                promotion = Promotion.objects.get(name__iexact=promo_name, department=department)
            except:
                continue

            Student.objects.update_or_create(
                matricule=matricule,
                defaults={
                    'nom': nom,
                    'postnom': postnom,
                    'prenom': prenom,
                    'promotion': promotion,
                    'department': department,
                    'vacation': str(row.get('vacation') or 'jour').lower()
                }
            )

            created += 1

        return render(request, 'academics/import_success.html', {
            "count": created
        })

    return render(request, 'academics/import_students.html')


def admin_required(user):
    return user.is_superuser


from academics.models import Promotion

def admin_home(request):
    promotions = Promotion.objects.all()
    sections = Section.objects.all()
    departments = Department.objects.all()

    return render(request, "deliberation/admin/home.html", {
        "promotions": promotions,
        'sections': sections,
        'departments':departments
    })
def admin_dashboard(request):
    promotions = Promotion.objects.all()
    
    return render(request, 'deliberation/admin/dashboard.html', {
        'promotions': promotions
        
    })


from django.db.models import Prefetch

def admin_deliberation_view(request):

    promotion_id = request.GET.get("promotion")
    department_id = request.GET.get("department")
    section_id = request.GET.get("section")

    students = Student.objects.select_related(
        "promotion", "department", "department__section"
    )

    if promotion_id:
        students = students.filter(promotion_id=promotion_id)

    if department_id:
        students = students.filter(department_id=department_id)

    if section_id:
        students = students.filter(department__section_id=section_id)

    courses = Course.objects.select_related("ue").filter(
        promotion_id=promotion_id
    )

    grades = Grade.objects.filter(
        student__in=students,
        course__in=courses
    ).select_related("course", "course__ue", "student")

    results = []

    for student in students:

        total_credit = 0
        total_tnp = 0
        validated_credit = 0
        dettes = []

        for course in courses:

            grade = grades.filter(student=student, course=course).first()

            note = grade.note_finale if grade and grade.note_finale else 0
            credit = course.credit

            if note >= 10:
                validated_credit += credit
                total_tnp += note * credit
            else:
                dettes.append(course)

            total_credit += credit

        moyenne = total_tnp / total_credit if total_credit else 0

        # 🎯 LOGIQUE LMD
        if validated_credit >= 45:
            decision = "PA"
        else:
            decision = "PP"

        results.append({
            "student": student,
            "moyenne": round(moyenne, 2),
            "credits": validated_credit,
            "decision": decision,
            "dettes": dettes
        })

    return render(request, "deliberation/admin/students.html", {
        "results": results,
        "promotions": Promotion.objects.all(),
        "departments": Department.objects.all(),
        "sections": Section.objects.all()
    })

def admin_student_detail(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    result = calcul_deliberation(student)

    # 🔥 récupérer dettes (cours < 10)
    dettes = []
    for ue in result['ues']:
        for c in ue['courses']:
            if c['note'] < 10:
                dettes.append(c['course'])

    return render(request, "deliberation/admin/student_detail.html", {
        "student": student,
        "ues": result['ues'],
        "moyenne": result['moyenne'],
        "credits_valides": result['credits'],
        "decision": result['decision'],
        "dettes": dettes
    })

def admin_courses(request):
    courses = Course.objects.all()
    return render(request, 'deliberation/admin/courses.html', {
        'courses': courses
    })


def admin_assignments(request):
    assignments = CourseAssignment.objects.select_related('teacher', 'course')
    return render(request, 'deliberation/admin/assignments.html', {
        'assignments': assignments
    })


def admin_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'deliberation/admin/teachers.html', {
        'teachers': teachers
    })


def admin_ues(request):
    ues = UE.objects.all()
    return render(request, 'deliberation/admin/ues.html', {
        'ues': ues
    })

