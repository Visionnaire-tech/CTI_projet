from django.urls import path
from . import views 
from . import views_admin
from .views import custom_logout
from deliberation.views import admin_deliberation_view
from deliberation.excel import export_deliberation_excel
from django.contrib.auth import views as auth_views
from .views import admin_deliberation_view, student_login, student_dashboard, export_excel_view

urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='password_reset'),#, email_template_name='accounts/password_reset_email.html'

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('result/', views.student_result, name='student_result'),
    path('admin/dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admin/student/<int:student_id>/', views_admin.admin_student_detail, name='admin_student_detail'),
    path('admin/deliberation/', admin_deliberation_view, name='admin_deliberation'),
    path('login/', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('logout/', custom_logout, name='logout'),
    path('export-excel/<int:promotion_id>/', export_excel_view, name='export_excel'),
    path('deliberation/<int:promotion_id>/', admin_deliberation_view, name='admin_deliberation'),
    path('export-excel/<int:promotion_id>/', export_deliberation_excel, name='export_excel'),

]