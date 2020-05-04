from django import forms
from .models import Project, Status, Comment, Task
import datetime
from django.contrib.auth.models import User


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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)
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


# TODO Vérifier niveau serveur que start_date < due_date et que les membres soient bien du projet
class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('project', 'comments',)
        widgets = {
            'name' : text_widget,
            'description' : large_txt_widget,
            'status' : forms.RadioSelect(),
        }


    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Pour que y ait pas le champ "------"
        self.fields['user'].empty_label = None
        self.fields['status'].empty_label = None

        # Pour que les membres selectionnables ne soient que ceux du projet
        project = kwargs['initial']['project']
        self.fields['user'].queryset = project.members
