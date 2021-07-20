from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    class Meta:
        model = MedUser
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


# User Registration form for Worker
class UserRegistrationForm1(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = MedUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


# User Registration form for Patient
class UserRegistrationForm2(MyUserCreationForm):
    password1 = None
    password2 = None

    class Meta:
        model = MedUser
        fields = ['first_name', 'last_name']


class WorkerRegistrationForm(ModelForm):
    class Meta:
        model = Worker
        fields = ['age', 'gender', 'cadre', 'dept']


class PatientRegistrationForm(ModelForm):
    

    class Meta:
        model = Patient
        fields = ['age', 'gender', 'weight', 'height', 'ward', 'lga', 'state', 'picture']


class EncounterCreationForm(ModelForm):
    patient_username = forms.CharField(max_length=150)

    class Meta:
        model = Encounter
        fields = ['patient_username','date', 'time', 'visit', 'weight', 'height', 'bp', 'temp', 'rr', 'complaints','diagnosis', 'treatment_plan']