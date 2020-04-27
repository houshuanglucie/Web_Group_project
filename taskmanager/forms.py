from django import forms
from .models import Project, Status, Comment, Task

text_widget = forms.TextInput(
    attrs = {
        'class' : 'form-control',
        'required' : "True"
    })



class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'members')
        widgets = {
            'name' : text_widget
        }
