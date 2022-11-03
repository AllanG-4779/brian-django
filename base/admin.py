from django.contrib import admin

from .models import TeacherRegistration, StudentRegistration, Class, Subject, Exam, Term
# Register your models here.
admin.site.register(TeacherRegistration)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Term)
admin.site.register(StudentRegistration)