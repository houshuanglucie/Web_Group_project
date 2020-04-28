from django import forms
from .models import Project, Status, Comment, Task

text_widget = forms.TextInput(
    attrs = {
        'class' : 'form-control',
        'required' : "True"
    })

large_txt_widget = forms.Textarea(
    attrs = {
        'class' : 'form-control',
        'rows' : 4
    })



class LoginForm(forms.Form):
    username = forms.CharField(label = "Nom d'utilisateur", max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'rows' : '1',
                'placeholder' : "Nom d'utilisateur"
            }
        ))
    password = forms.CharField(label="Mot de passe",
        widget = forms.PasswordInput(
            attrs = {
                'rows' : '1',
                'placeholder' : "Mot de passe"
            }
        ))

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'members')
        widgets = {
            'name' : text_widget
        }
# TODO Mettre le champ user required

class ManageProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'members')
        widgets = {
            'name' : text_widget
        }


class CommentForm(forms.Form):
    content = forms.CharField(label="Commentaire",
        widget = forms.Textarea(
            attrs = {
                'rows' : '1',
                'class' : 'form-control',
                'placeholder' : "Ajouter un commentaire"
            }
        ))
