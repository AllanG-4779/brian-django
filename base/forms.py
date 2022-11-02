from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from base.models import TeacherRegistration
from django import forms

from django.contrib.auth.models import User


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = [ "username",
                  "email", "password1", "password2"]


class TeacherCreationForm(ModelForm):
    CHOICES = [("Mr", "Mr"), ("Mrs", "Mrs"), ("Miss", "Miss"), ]
    tittle = forms.ChoiceField(
        choices=CHOICES,  widget=forms.RadioSelect(),)
    dateofbirth = forms.DateField(widget=forms.DateTimeInput(
        attrs={"type": "date"}))

    class Meta:
        model = TeacherRegistration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeacherCreationForm, self).__init__(*args, **kwargs)

        for items in self.fields.values():
            items.widget.attrs["class"] = "form-control form-control-sm"
