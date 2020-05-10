from django import forms
from .models import Project, Status, Comment, Task
import datetime
from django.contrib.auth.models import User

text_widget = forms.TextInput(
    attrs={
        'class': 'form-control',
        'required': "True"
    })

large_txt_widget = forms.Textarea(
    attrs={
        'class': 'form-control',
        'rows': 4
    })


# Form pour se connecter
class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30,
                               widget=forms.TextInput(
                                   attrs={
                                       'rows': '1',
                                       'class': 'form-control',
                                       'placeholder': "Nom d'utilisateur"
                                   }
                               ))
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'rows': '1',
                                       'class': 'form-control',
                                       'placeholder': "Mot de passe"
                                   }
                               ))


# Form de création ou modification de projet
class ProjectForm(forms.ModelForm):
    # On ne met pas le field members, je le crée moi meme avec un drag & drop en js
    class Meta:
        model = Project
        fields = ('name',)
        widgets = {
            'name': text_widget
        }


# Form pour ajouter un commentaire a une tache
class CommentForm(forms.Form):
    content = forms.CharField(label="Commentaire",
                              widget=forms.Textarea(
                                  attrs={
                                      'rows': '1',
                                      'class': 'form-control',
                                      'placeholder': "Ajouter un commentaire"
                                  }
                              ))


# Form pour ajouter ou modifier une tache
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('project', 'comments',)
        widgets = {
            'name': text_widget,
            'description': large_txt_widget,
            'status': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Pour que y ait pas le champ "------"
        self.fields['user'].empty_label = None
        self.fields['status'].empty_label = None

        # Pour que les membres selectionnables ne soient que ceux du projet
        project = kwargs['initial']['project']
        self.fields['user'].queryset = project.members

    def clean(self):
        # A priori inutile si mon cote client est bien fait, mais toujours bien d'avoir une autre verification niveau serveur...
        cleaned_data = super(TaskForm, self).clean()

        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if (start_date > due_date):
            self.add_error("start_date",
                           "Vérifiez vos dates : la date de début doit être avant la date de fin (Logique non ?)")

        return cleaned_data


class CompletedForm(forms.Form):
    completed = forms.IntegerField(required=False)
