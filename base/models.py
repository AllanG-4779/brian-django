from django.db import models
from django.contrib.auth.models import User

# Create models here.


class TeacherRegistration(models.Model):
   
    year_employed = models.CharField(max_length=4, null=False)
    national_id = models.CharField(max_length=8, unique=True, null=False)
    gender = models.CharField(max_length=10, null=False)
    dob = models.DateField()
    address = models.CharField(max_length=20, null=False)
    phone_number = models.CharField(max_length=10, null=False)  
    auth_id = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None)
    def __str__(self) :
        return self.auth_id.first_name +" " + self.auth_id.last_name
        


class Subject(models.Model):
    subjectID = models.CharField(max_length=3,  unique=True, primary_key=True)
    subjectname = models.CharField(max_length=15, unique=True)


class Class(models.Model):
    classID = models.CharField(max_length=3, unique=True)
    classname = models.CharField(max_length=10, unique=True)
    classteacher = models.OneToOneField(
        TeacherRegistration, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.classname
    


class StudentRegistration(models.Model):

  
    year_of_admission = models.CharField(max_length=4, null=False)
    date_of_birth= models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=6, null=False)
    level = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    auth_id = models.OneToOneField(
        User, on_delete=models.CASCADE, default=None)


class Term(models.Model):
    termname = models.CharField(max_length=10)
    academicyear = models.CharField(max_length=4)

    class Meta:
        unique_together = ('termname', 'academicyear')


class Exam(models.Model):
    examtype = models.CharField(max_length=10)
    studentID = models.ForeignKey(
        StudentRegistration, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING)
    marks = models.IntegerField(null=False, default=0)

    class Meta:
        unique_together = ("examtype", "studentID", "subject", "term")
