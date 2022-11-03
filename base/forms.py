from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from base.models import TeacherRegistration
from django import forms

from django.contrib.auth.models import User


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', "username", "email", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for items in self.fields.values():
            items.widget.attrs['class'] = "form-control form-control-sm flex"


class TeacherCreationForm(ModelForm):
    CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other"), ]
    gender = forms.ChoiceField(
        choices=CHOICES,  widget=forms.RadioSelect(),)
    dob = forms.DateField(widget=forms.DateTimeInput(
        attrs={"type": "date"}))

    class Meta:
        model = TeacherRegistration
        fields = ['gender', 'dob', 'year_employed', 'phone_number', 'national_id', 'address']

    def __init__(self, *args, **kwargs):
        super(TeacherCreationForm, self).__init__(*args, **kwargs)

        for items in self.fields.values():
            items.widget.attrs["class"] = "form-control form-control-sm"
