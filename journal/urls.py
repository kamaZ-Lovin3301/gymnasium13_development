from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('', views.teacher_journal, name='teacher_journal'),
    path('class/<int:class_id>/', views.select_subject, name='select_subject'),
    path('class/<int:class_id>/subject/<int:subject_id>/', views.journal_page, name='journal_page'),
    path('api/set_grade/', views.set_grade, name='set_grade'),
    path('api/set_homework/', views.set_homework, name='set_homework'),
    path('teacher/schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('student/schedule/', views.student_schedule, name='student_schedule'),
    path('student/diary/', views.student_diary, name='student_diary'),
    path('student/quarter-grades/<int:student_id>/', views.quarter_grades, name='quarter_grades'),
]