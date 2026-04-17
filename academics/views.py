import pandas as pd
from django.shortcuts import render
from .models import Student, Promotion, Department, Section, UE
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from courses.models import Teacher, Course
from deliberation.views import student_result
from evaluations.models import Grade


def normalize(col):
    return col.strip().lower()


def import_students(request):
    if request.method == 'POST':
        file = request.FILES['file']

        df = pd.read_excel(file)

        # normaliser colonnes
        df.columns = [normalize(c) for c in df.columns]

        for _, row in df.iterrows():

            matricule = row.get('matricule') or row.get('id')
            nom = row.get('nom') or row.get('name')
            prenom = row.get('prenom') or row.get('firstname')

            promo_name = row.get('promotion') or row.get('classe')
            dept_name = row.get('department') or row.get('section')

            try:
                promo = Promotion.objects.get(name=promo_name)
                dept = Department.objects.get(name=dept_name)
            except:
                continue

            Student.objects.update_or_create(
                matricule=matricule,
                defaults={
                    'nom': nom,
                    'prenom': prenom,
                    'promotion': promo,
                    'department': dept,
                    'vacation': row.get('vacation', 'Jour')
                }
            )

        return render(request, 'academics/import_success.html')

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


def admin_deliberation_view(request):

    promotion_id = request.GET.get("promotion")
    department_id = request.GET.get("department")
    section_id = request.GET.get("section")

    students = Student.objects.all()

    # 🔍 FILTRES
    if promotion_id:
        students = students.filter(promotion_id=promotion_id)

    if department_id:
        students = students.filter(department_id=department_id)

    if section_id:
        students = students.filter(department__section_id=section_id)

    ues = UE.objects.all().prefetch_related('course_set')

    results = []

    for student in students:
        total_tnp = 0
        total_credit = 0

        for ue in ues:
            for course in ue.course_set.all():

                grade = Grade.objects.filter(student=student, course=course).first()

                note = grade.note_finale if grade and grade.note_finale else 0
                credit = course.credit
                tnp = note * credit

                total_tnp += tnp
                total_credit += credit

        # 📊 MOYENNE
        moyenne = total_tnp / total_credit if total_credit else 0

        # 🎯 DECISION
        if moyenne >= 10:
            decision = "ADM"
        elif moyenne >= 8:
            decision = "AJ"
        else:
            decision = "DEF"

        results.append({
            "student": student,
            "moyenne": round(moyenne, 2),
            "credits": total_credit,  # ✅ AJOUT IMPORTANT
            "decision": decision
        })

    return render(request, "deliberation/admin/students.html", {
        "results": results,
        "promotions": Promotion.objects.all(),
        "departments": Department.objects.all(),
        "sections": Section.objects.all()
    })

def admin_student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'deliberation/admin/student_detail.html', {
        'student': student
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

