from django.shortcuts import render
from base.models import StudentRegistration
from base.models import TeacherRegistration
from base.models import Class
from base.models import Subject
from base.models import Exam
from base.models import Term

from base.forms import TeacherCreationForm, SignupForm, StudentCreationform


def HomePage(request):

    return render(request, 'base/HomePage.html')


def LoginPage(request):
    return render(request, 'base/LoginPage.html')


def StudentHomePage(request):
    return render(request, 'base/StudentHomePage.html')


def TeacherRegPage(request):
    success = ""

    signup_form  = SignupForm(request.POST)
    teacher_creation  = TeacherCreationForm(request.POST)

    if signup_form.is_valid():
        
        success= "auth is valid"
        if teacher_creation.is_valid():
           success="both are valid"
           
           user = signup_form.save(commit=True)
           user.is_staff=True
           user.save()
           teacher = teacher_creation.data
           TeacherRegistration(auth_id=user, phone_number=teacher.get('phone_number'),
            year_employed=teacher.get('year_employed'),address=teacher.get('address'),
             dob=teacher.get('dob'),national_id=teacher.get('national_id'),
              gender = teacher.get('gender')).save()       
           success = "User Created successfully"
        else:
            print(teacher_creation.non_field_errors.__get__('phone_number'))
            success="Some additional details were not validated"
            return render(request, "base/TeacherRegPage.html",
             {"teacher_creation":teacher_creation, "signup_form":signup_form, "success":success})
    else:
        success = "User not created, check you inputs and try again"
   
    return render(request, 'base/TeacherRegPage.html',
     {"auth_form": signup_form, "teacher_creation": teacher_creation, "success": success})


def StudentRegPage(request):
    registration_status = {}
    student_signup = SignupForm(request.POST)
    student_creation = StudentCreationform(request.POST)
    # if (request.method == "POST"):
    #     firstname = request.POST['firstname']
    #     lastname = request.POST['lastname']
    #     regNo = request.POST['regNo']
    #     yearofAdmission = request.POST['yearofAdmission']
    #     gender = request.POST['gender']
    #     level = request.POST['level']
    #     date = request.POST['date']
    #     # import the model and create an object
    #     my_current_class = Class.objects.filter(classname=level).first()
    #     print(my_current_class)

    #     student = StudentRegistration(date=date, firstname=firstname, lastname=lastname,
    #                                   yearofAdmission=yearofAdmission, gender=gender, level=my_current_class, regNo=regNo)
    #     student.save()
    #     registration_status["success"] = "Successfully registered"

    return render(request, 'base/StudentRegPage.html', { "student_signup":student_signup, "student_creation":student_creation})


def TeacherHomePage(request):
    return render(request, 'base/TeacherHomePage.html')


def PrincipalHomePage(request):
    return render(request, 'base/PrincipalHomePage.html')


def StudentProfile(request):
    return render(request, 'base/StudentProfile.html',)


def TeacherProfile(request):
    Teacher = TeacherRegistration.objects.filter(nationalid="32322322").first()

    if request.method == "PUT":
        Firstname = request.POST['firstname']
        Lastname = request.POST['lastname']
        TSCNumber = request.POST['tscnumber']
        YearEmployed = request.POST['yearemployed']
        NationalID = request.POST['nationalid']
        Tittle = request.POST['tittle']
        DateofBirth = request.POST['dateofbirth']
        Address = request.POST['address']
        PhoneNumber = request.POST['phonenumber']
        EmailAddress = request.POST['emailaddress']

        teacher = TeacherRegistration(firstname=firstname)
        teacher.save()

    return render(request, 'base/TeacherProfile.html', {"User": Teacher})


def MarkEntry(request):
    subjects_query = Subject.objects.all()
    # Get all the subject in a specific form from the authenticated teacher
    # for now use student from form 2
    class_of_logged_in_teacher = Class.objects.filter(classteacher=2).first()
    studentList = StudentRegistration.objects.filter(
        level=class_of_logged_in_teacher).all()

    subjects = [x.subjectname for x in subjects_query.all()]
    active_student = None
    if request.method == "PUT":
        search_admission = request.PUT.get("admission")
        studentList = studentList.filter(regNo=search_admission)

    if request.method == "GET":
        Admission = request.GET.get("admission")
        active_student = StudentRegistration.objects.filter(
            regNo=Admission).first()

        if not active_student:
            message = "Student not found, Ensure the student belong to your class"
            return render(request, "base/MarkEntry.html", {"search": message, "studentList": studentList})

    marks_status = {}
    if request.method == "POST":

        admission_no = request.POST.get("admission")

        active_student = StudentRegistration.objects.filter(
            regNo=admission_no).first()
        SelectExamType = request.POST.get('exam_type')
        BUSINESS = request.POST.get('BUSINESS')
        CHEMISTRY = request.POST.get('CHEMISTRY')
        CRE = request.POST.get('CRE')
        ENGLISH = request.POST.get('ENGLISH')
        GEOGRAPHY = request.POST.get('GEOGRAPHY')
        KISWAHILI = request.POST.get('KISWAHILI')
        MATHEMATICS = request.POST.get('MATHEMATICS')
        PHYSICS = request.POST.get('PHYSICS')
        BIOLOGY = request.POST.get('BIOLOGY')
        AGRICULTURE = request.POST.get('AGRICULTURE')
        HISTORY = request.POST.get('HISTORY')
        MUSIC = request.POST.get('MUSIC')
        COMPUTERSTUDIES = request.POST.get('COMPUTER STUDIES')

        student_marks = []
        if not(BUSINESS is None):
            student_marks.append({"BUSINESS": BUSINESS})
        if not(CHEMISTRY is None):
            student_marks.append({"CHEMISTRY": CHEMISTRY})
        if not(CRE is None):
            student_marks.append({"CRE": CRE})
        if not(ENGLISH is None):
            student_marks.append({"ENGLISH": ENGLISH})
        if not(GEOGRAPHY is None):
            student_marks.append({"GEOGRAPHY": GEOGRAPHY})
        if not(KISWAHILI is None):
            student_marks.append({"KISWAHILI": KISWAHILI})
        if not(MATHEMATICS is None):
            student_marks.append({"MATHEMATICS": MATHEMATICS})
        if not(PHYSICS is None):
            student_marks.append({"PHYSICS": PHYSICS})
        if not(BIOLOGY is None):
            student_marks.append({"BIOLOGY": BIOLOGY})
        if not(AGRICULTURE is None):
            student_marks.append({"AGRICULTURE": AGRICULTURE})
        if not(HISTORY is None):
            student_marks.append({"HISTORY": HISTORY})
        if not(MUSIC is None):
            student_marks.append({"MUSIC": MUSIC})
        if not(COMPUTERSTUDIES is None):
            student_marks.append({"COMPUTER STUDIES": COMPUTERSTUDIES})

        term = Term.objects.all().filter(academicyear='2022', termname="ONE").first()

        print(student_marks)
        for student_mark in student_marks:
            subject = Subject.objects.filter(
                subjectname=list(student_mark.keys())[0]).first()
            MarkEntry = Exam(examtype=SelectExamType,
                             studentID=active_student, term=term, subject=subject, marks=int(list(student_mark.values())[0]))
            MarkEntry.save()

        marks_status["success"] = f"Successfully uploaded marks for  {len(student_marks)} subjects"

    message = "Done"
    return render(request, "base/MarkEntry.html", {"subjects": subjects, "student": active_student, "search": "", "studentList": studentList})


def StudentAcademics(request):
    if request.method == "GET":
        Code = request.GET.get("subjectID")
        subjects = Subject.objects.all()
    return render(request, 'base/StudentAcademics.html', {"subjects": subjects})


def Reportform(request):
    return render(request, 'base/Reportform.html')
