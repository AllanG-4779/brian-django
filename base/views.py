from django.shortcuts import render
from base.models import StudentRegistration
from base.models import TeacherRegistration
from base.models import Class
from base.models import Subject
from base.models import Exam
from base.models import Term
from django.shortcuts import redirect
from django.contrib.auth  import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from base.forms import TeacherCreationForm, SignupForm, StudentCreationform

@login_required(login_url="/LoginPage")
def HomePage(request):
    user = request.user
    if(user.is_staff and (not user.is_superuser)):
        return redirect('teacherHomepage')
    if(user):
        return redirect('studentHomepage')
    if(user.is_superuser):
        return redirect("principalHomepage")

    return render(request, 'base/HomePage.html')

def user_logout(request):
    logout(request)
    return redirect("login")

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username is not None and password is not None:
            print(username+" " + password)
            user = authenticate(request=request, username=username, password =password)
            print(user)
            if user is not None:
                login(request=request, user=user)
                return redirect("/")
            else:
                return render(request, "base/LoginPage.html", {"message": "Wrong username or password"})

    return render(request, 'base/LoginPage.html')

@login_required(login_url="login")
def StudentHomePage(request):
    
    return render(request, 'base/StudentHomePage.html')

@login_required(login_url="login")
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
            print(teacher_creation.errors)
            success="Some additional details were not validated"
            return render(request, "base/TeacherRegPage.html",
             {"teacher_creation":teacher_creation, "signup_form":signup_form, "success":success})
    else:
        print(signup_form.errors)
        success = "User not created, check you inputs and try again"
   
    return render(request, 'base/TeacherRegPage.html',
     {"auth_form": SignupForm(), "teacher_creation": TeacherCreationForm(), "success": success})

@login_required(login_url='login')
def StudentRegPage(request):
    registration_status = {}
    student_signup = SignupForm(request.POST)
    student_creation = StudentCreationform(request.POST)
    if(student_creation.is_valid() and student_signup.is_valid()):   
        student_creation_content = student_creation.data
        auth_student = student_signup.save(commit=True)
        print(auth_student)
        print(student_creation_content.get('level'))
        
        
        
        student = StudentRegistration(
            year_of_admission = student_creation_content.get('year_of_admission'),
            date_of_birth= student_creation_content.get('date_of_birth'),
            gender=student_creation_content.get('gender'),
            level=Class.objects.all().filter(id=int(student_creation_content.get('level'))).first(),
            auth_id=auth_student
        )
        student.save()
    else:
        print(student_creation.errors)
        print(student_signup.errors)
      
    

    return render(request, 'base/StudentRegPage.html', { "student_signup":student_signup, "student_creation":student_creation})

@login_required(login_url='login')
def TeacherHomePage(request):
    return render(request, 'base/TeacherHomePage.html')

@login_required(login_url='login')
def PrincipalHomePage(request):
    if not request.user.is_superuser:
        return redirect("/")
    return render(request, 'base/PrincipalHomePage.html')

@login_required(login_url='login')
def StudentProfile(request):
    return render(request, 'base/StudentProfile.html',)

@login_required(login_url='login')
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

@login_required
def MarkEntry(request):
    subjects_query = Subject.objects.all()
    # Get all the subject in a specific form from the authenticated teacher
    # for now use student from form 2
    user_id = request.user.id
    logged_in_teacher = TeacherRegistration.objects.filter(auth_id=user_id).first()
    if logged_in_teacher is None:
        return redirect("/")
    print(type(logged_in_teacher.id))
    class_of_logged_in_teacher = Class.objects.filter(classteacher=(logged_in_teacher.id)).get()
    print(class_of_logged_in_teacher.classID)

    studentList = StudentRegistration.objects.all().filter(level=class_of_logged_in_teacher.id)


    subjects = [x.subjectname for x in subjects_query.all()]
    active_student = None
    if request.method == "PUT":
        search_admission = request.PUT.get("admission")
        studentList = studentList.filter(auth_id=search_admission).get()

    if request.method == "GET":
        Admission = request.GET.get("admission")
        
        active_student = StudentRegistration.objects.all().filter(
            auth_id=User.objects.all().filter(username=Admission).first())

        if not active_student:
            message = "Student not found, Ensure the student belong to your class"
            return render(request, "base/MarkEntry.html", {"search": message, "studentList": studentList})

    marks_status = {}
    if request.method == "POST":

       
        SelectExamType = request.POST.get('exam_type')
        BUSINESS = request.POST.get('')
        CHEMISTRY = request.POST.get('CHEMISTRY')
        CRE = request.POST.get('CRE')
        ENGLISH = request.POST.get('ENGLISH')
        GEOGRAPHY = request.POST.get('GEOGRAPHY')
        # KISWAHILI = request.POST.get('KISWAHILI')
        # MATHEMATICS = request.POST.get('MATHEMATICS')
        # PHYSICS = request.POST.get('PHYSICS')
        # BIOLOGY = request.POST.get('BIOLOGY')
        # AGRICULTURE = request.POST.get('AGRICULTURE')
        # HISTORY = request.POST.get('HISTORY')
        # MUSIC = request.POST.get('MUSIC')
        # COMPUTERSTUDIES = request.POST.get('COMPUTER STUDIES')

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

@login_required(login_url='login')
def StudentAcademics(request):
    if request.method == "GET":
        Code = request.GET.get("subjectID")
        subjects = Subject.objects.all()
    return render(request, 'base/StudentAcademics.html', {"subjects": subjects})

@login_required(login_url='login')
def Reportform(request):
    return render(request, 'base/Reportform.html')
