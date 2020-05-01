from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import LoginForm, ProjectForm, CommentForm, ProjectForm, TaskForm
from .models import Project, Status, Comment, Task, Category, Subtask

import datetime
import json

# =============== Page d'accueil =================
@login_required(login_url = 'connect')
def home(request):
    try:
        if request.session['just_log']: # Pour afficher un toast
            new_log = True
        else:
            new_log = False
    except:
        new_log = False
    request.session['just_log'] = False

    return render(request, 'taskmanager/home.html', locals())


# ***************************************************************************
#  USER AUTHENTIFICATION
# ***************************************************************************

# =============== Page de redirection vers l'accueil =================
@login_required(login_url = 'connect')
def redirect_home(request):
    return redirect('home')


# =============== Page de connexion =================
def connect(request):
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                request.session['just_log'] = True
                return redirect('home')
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'taskmanager/connect.html', locals())


# =============== "Page" de deconnextion =================
# On redirige directement vers la page de connexion
@login_required(login_url = 'connect')
def disconnect(request):
    logout(request)
    return redirect('connect')



# ***************************************************************************
#  PROJECTS MANAGER
# ***************************************************************************

# =============== Page de vue de mes projets  =================
@login_required(login_url = 'connect')
def projects(request):
    current_user = User.objects.get(id = request.user.id)
    projects_list = Project.objects.filter(Q(members = current_user) | Q(public = "PU")).distinct()

    print(str(projects_list.query), flush = True)

    if(request.session.get('new_delete') != None):
        deleted_project = request.session.get('new_delete')
        request.session['new_delete'] = None
        show_toast = True
    else:
        deleted_project = None
        show_toast = False

    return render(request, 'taskmanager/projects.html', locals())



# =============== Page de vue d'un projet =================
@login_required(login_url = 'connect')
def focus_project(request, id):
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project__id = id).order_by('priority', '-due_date')

    # Si on vient de supprimer une tache, pour qu'on ait un toast qui apparaisse
    if(request.session.get('new_delete') != None):
        deleted_task = request.session.get('new_delete')
        request.session['new_delete'] = None
        show_toast = True
    else:
        deleted_project = None
        show_toast = False

    return render(request, 'taskmanager/focus_project.html', locals())



# =============== Page de création d'un nouveau projet =================
@login_required(login_url = 'connect')
def newproject(request):
    added = False
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        members = form.cleaned_data['members']
        project = Project(name = name)
        if("publicCheck" in request.POST):
            project.public = "PU"
        else:
            project.public = "PR"
        project.save()
        project.members.set(members)
        project.save()
        added = True

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "ADD")

    return render(request, 'taskmanager/formproject.html', locals())


# ***************************************************************************
#  TASKS MANAGER
# ***************************************************************************

# =============== Page de modification/suppression d'un projet =================
@login_required(login_url = 'connect')
def manageproject(request, id):
    added = False
    project = Project.objects.get(id = id)

    defaults = {'name' : project.name} # prepopulationner les champs
    defaults['members'] = [m for m in project.members.all()]
    form = ProjectForm(request.POST or None, initial = defaults)

    if form.is_valid():
        if('delete' in request.POST):
            request.session['new_delete'] = project.name
            project.delete()
            return redirect('projects')
        elif('save' in request.POST):
            if("publicCheck" in request.POST):
                project.public = "PU"
            else:
                project.public = "PR"
            project.name = form.cleaned_data['name']
            project.members.set(form.cleaned_data['members'])
            project.save()
            added = True

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "MODIFY")

    return render(request, 'taskmanager/formproject.html', locals())





# =============== Page de vue d'une tache =================
@login_required(login_url = 'connect')
def focus_task(request, id):
    task = Task.objects.get(id = id)
    comments = task.comments.all().order_by('-submit_time')


    subtasks = Subtask.objects.filter(task = task).order_by("id")

    # Si on vient de modifier une tache, pour qu'on ait un toast qui apparaisse
    if(request.session.get('new_modify') != None):
        modified_task = request.session.get('new_modify')
        request.session['new_modify'] = None
        show_toast = True
    else:
        modified_task = None
        show_toast = False

    # Affichage de la pièce jointe
    att_name, att_extension = task.attachment_info()
    show_as_picture = att_extension in [".jpg", ".png"]
    show_as_doc = att_extension in [".pdf", ".txt"]

    # Gestion des commentaires
    form_comment = CommentForm(request.POST or None)

    if form_comment.is_valid():
        new_comment = Comment(user = request.user, content = form_comment.cleaned_data['content'])
        new_comment.save()
        task.comments.add(new_comment)
        task.save()

    return render(request, 'taskmanager/focus_task.html', locals())


# =============== Validation de la création/modification d'une tache =================
# Pas possible de le faire comme un clean parce que y a du javascript qui vient tout chambouler.
# Du moins, je n'en ai pas l'impression
def validate_task_data(task, request, form, project, action):
    #   args :
    #       task            Tache a valider
    #       request         Le request... dont on va exploiter le POST pour recuperer les champs crées par js
    #       form            Le formulaire pour avoir les cleaned_data
    #       project         Projet parent de la tache (necessaire notamment pour la creation de tache)
    #       action          "ADD" ou "MODIFY" (pour savoir que faire des subtasks)
    #   returns :
    #       added           Boolean pour afficher le toast par la suite
    #       error_category  Si l'user fait n'importe quoi avec le champ category
    #       task            Tache validee ou None (en soi, j'ai juste besoin du nom pour l'afficher sur le toast)

    error_category = False
    added = True

    # Normal fields
    task.project = project
    task.name = form.cleaned_data['name']
    task.description = form.cleaned_data['description']
    task.user = form.cleaned_data['user']
    task.attachment = form.cleaned_data['attachment']
    task.start_date = form.cleaned_data['start_date']
    task.due_date = form.cleaned_data['due_date']
    task.priority = form.cleaned_data['priority']
    task.status = form.cleaned_data['status']


    # Champ category : non required, mais si existe, on va le cherche dans le request.POST
    if('new_category' in request.POST and request.POST['new_category'] != '' and request.POST['category'] != ''):
        added = False
        error_category = True
        return added, error_category, None
    elif('new_category' in request.POST and request.POST['new_category'] != '' and request.POST['category'] == ''):
        new_category = Category(name = request.POST['new_category'])
        new_category.save()
        task.category = new_category
    else:
        task.category = form.cleaned_data['category']

    task.save()


    # Subtasks : pas un champ de task, mais dépend quand meme de task
    if(action == "ADD"):
        if('new_subtask' in request.POST):
            for subtask in request.POST.getlist('new_subtask'):
                if(subtask != ''):
                    new_subtask = Subtask(task = task, name = subtask)
                    new_subtask.save()

    elif(action == "MODIFY"):
        former_subtasks = Subtask.objects.filter(task = task)

        if('new_subtask' in request.POST):
            for subtask in request.POST.getlist('new_subtask'):
                if(subtask != ''):
                    if (former_subtasks.filter(name = subtask).count() == 1):
                        continue # La subtask dans le formulaire était deja dans les anciennes subtask
                    else: # Sinon, a priori, le count = 0, alors on cree la nouvelle subtask
                        new_subtask = Subtask(task = task, name = subtask)
                        new_subtask.save()
            for subtask in former_subtasks:
                if subtask.name not in request.POST.getlist('new_subtask'):
                    subtask.delete()
        else:
            for subtask in former_subtasks:
                subtask.delete()



    return added, error_category, task




# =============== Page de création de tâche =================
@login_required(login_url = 'connect')
def newtask(request, id_project):
    added = False
    error_category = False

    project = Project.objects.get(id = id_project)
    defaults = {'status' : Status.objects.all()[0]}

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial = defaults)
        if form.is_valid():
            new_task = Task()
            added, error_category, new_task = validate_task_data(new_task, request, form, project, "ADD")
    else:
        form = TaskForm(initial = defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "ADD")
    start_date_format = due_date_format = ""

    return render(request, 'taskmanager/formtask.html', locals())



# =============== Page de modification/suppression d'une tache =================
def managetask(request, id):
    added = False
    error_category = False

    task = Task.objects.get(id = id)
    project = task.project

    start_date_format = task.start_date.strftime("%d/%m/%Y %H:%M")
    due_date_format = task.due_date.strftime("%d/%m/%Y %H:%M")

    subtasks = Subtask.objects.filter(task = task).order_by("id")
    subtask_list = [subtask.name for subtask in subtasks]
    subtask_list = json.dumps(subtask_list)


    defaults = {'name' : task.name,
                'description' : task.description,
                'user' : task.user,
                'priority' : task.priority,
                'status' : task.status,
                'category' : task.category,
                'attachment' : task.attachment}

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial=defaults)
        if form.is_valid():
            if('delete' in request.POST):
                request.session['new_delete'] = task.name
                task.delete()
                return redirect('focus_project', id = task.project.id)
            elif('save' in request.POST):
                added, error_category, task = validate_task_data(task, request, form, task.project, "MODIFY")
                if(not error_category):
                    request.session['new_modify'] = task.name
                    return redirect('focus_task', id = task.id)

    else:
        form = TaskForm(initial = defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "MODIFY")
    return render(request, 'taskmanager/formtask.html', locals())


# TODO Calendrier https://alexpnt.github.io/2017/07/15/django-calendar/
# https://medium.com/@unionproject88/django-and-python-calendar-e647a8eccff6
# https://www.geeksforgeeks.org/python-calendar-module/
