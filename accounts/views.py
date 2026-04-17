from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from academics.models import Student
from courses import views as course_views


def student_login(request):
    student = Student.objects.get(matricule=matricule)

    if not student.is_active:
        return render(request, 'accounts/student_login.html', {
            'error': 'Paiement non validé'
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('teacher_courses')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Identifiants incorrects'
            })

    return render(request, 'accounts/login.html')