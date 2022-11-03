from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.HomePage),
    path('LoginPage/', views.LoginPage, name="login"),
    path('student/home/page/', views.StudentHomePage, name="studentHomepage"),
    path('teacher/registration/', views.TeacherRegPage,
         name="teacherregistration"),
    path('student/registration/', views.StudentRegPage, name="registration"),
    path('teacher/home/page/', views.TeacherHomePage, name="teacherHomepage"),
    path('principal/home/page/', views.PrincipalHomePage, name="principalHomepage"),
    path('student/profile/', views.StudentProfile, name="studentprofile"),
    path('teacher/profile/', views.TeacherProfile, name="teacherprofile"),
    path("teacher/marks/entry", views.MarkEntry, name="markentry"),
    path("student/academics", views.StudentAcademics, name="academics"),
    path("report/form", views.Reportform, name="reportform"),
    path("logout", views.user_logout, name="logout")
]
urlpatterns += staticfiles_urlpatterns()
