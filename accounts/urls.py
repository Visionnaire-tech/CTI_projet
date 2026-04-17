from django.urls import path
from .views import login_view, student_login

urlpatterns = [
    path('login/', login_view, name='login'),
    path('student-login/', student_login),
]