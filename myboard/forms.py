from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from myboard.models import Profile, Task


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=50, required=False, help_text='Optional')
    username = forms.CharField(max_length=20, required=True, help_text='Required')

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class NewtaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']


class UpdateAssignForm(ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to']


class UpdateTextForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']


class UpdateStatusForm(ModelForm):
    class Meta:
        model = Task
        fields = ['status']
