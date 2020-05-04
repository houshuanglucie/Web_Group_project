from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.db.models import Q, Count
from django.http import JsonResponse
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
    print(request.session.get('new_delete'), flush = True)
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

    members = User.objects.all()
    members_of_project = []

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            list_members = request.POST.getlist('members[]')
            if list_members == []:
                return JsonResponse({"error": "No members"}, status=400)

            name = form.cleaned_data['name']
            project = Project(name = name)

            # Verification de l'aspect public ou privé
            if(request.POST.get("publicCheck") and request.POST.get("publicCheck")=='on'):
                project.public = "PU"
            else:
                project.public = "PR"
            project.save()

            # Ajout des membres
            for member in list_members:
                project.members.add(User.objects.get(username = member))
            project.save()

            # On répond à Ajax qui va se charger d'afficher le toast
            return JsonResponse({"state": "ok", "name" : name}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    else:
        form = ProjectForm()

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "ADD")

    return render(request, 'taskmanager/formproject.html', locals())


# ***************************************************************************
#  TASKS MANAGER
# ***************************************************************************

# =============== Page de modification/suppression d'un projet =================
@login_required(login_url = 'connect')
def manageproject(request, id):
    project = Project.objects.get(id = id)

    defaults = {'name' : project.name} # prepopulationner les champs
    members = []
    members_of_project = []

    for m in User.objects.all():
        if m in project.members.all():
            members_of_project.append(m)
        else:
            members.append(m)


    if request.method == 'POST':
        form = ProjectForm(request.POST, initial = defaults)

        if form.is_valid():
            # Si on a appuye sur le bouton delete, on lui repond que tout va bien, javascript va bien nous rediriger
            if(request.POST.get('action') and request.POST.get('action') == 'delete'):
                request.session['new_delete'] = project.name
                project.delete()
                return JsonResponse({"state": "ok"}, status=200)

            # Sinon, on modifie le projet
            elif(request.POST.get('action') and request.POST.get('action') == 'save'):
                list_members = request.POST.getlist('members[]')

                if list_members == []:
                    return JsonResponse({"error": "No members"}, status=400)

                project.name = form.cleaned_data['name']

                # Verification de l'aspect public ou privé
                if(request.POST.get("publicCheck") and request.POST.get("publicCheck")=='on'):
                    project.public = "PU"
                else:
                    project.public = "PR"
                project.save()

                # MaJ des membres
                project.members.clear()
                for member in list_members:
                    project.members.add(User.objects.get(username = member))

                project.save()
                # On répond à Ajax qui va se charger d'afficher le toast
                return JsonResponse({"state": "ok", "name" : project.name}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
    else:
        form = ProjectForm(initial = defaults)


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
@login_required(login_url = 'connect')
def validate_task_data(request, form, project, action, task = None):
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

    if(action == "ADD"):
        task = Task()


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



# TODO Mettre en membres que les membres du projet
# =============== Page de création de tâche =================
@login_required(login_url = 'connect')
def newtask(request, id_project):
    added = False
    error_category = False

    project = Project.objects.get(id = id_project)
    defaults = {'status' : Status.objects.all()[0], 'project' : project}

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial = defaults)
        if form.is_valid():
            added, error_category, new_task = validate_task_data(request, form, project, "ADD")
    else:
        form = TaskForm(initial = defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "ADD")
    start_date_format = due_date_format = ""

    return render(request, 'taskmanager/formtask.html', locals())



# =============== Page de modification/suppression d'une tache =================
@login_required(login_url = 'connect')
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
                'attachment' : task.attachment,
                'project' : project}

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial=defaults)
        if form.is_valid():
            if('delete' in request.POST):
                request.session['new_delete'] = task.name
                task.delete()
                return redirect('focus_project', id = task.project.id)
            elif('save' in request.POST):
                added, error_category, task = validate_task_data(request, form, task.project, "MODIFY", task)
                if(not error_category):
                    request.session['new_modify'] = task.name
                    return redirect('focus_task', id = task.id)

    else:
        form = TaskForm(initial = defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type = "MODIFY")
    return render(request, 'taskmanager/formtask.html', locals())


@login_required(login_url = 'connect')
def dashboard(request):
    current_user = User.objects.get(id = request.user.id)
    involved_projects = Project.objects.filter(members = current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks_by_proj_data = dict(project = project, tasks = Task.objects.filter(user = current_user, project = project))
        tasks_by_project.append(tasks_by_proj_data)

    print(tasks_by_project, flush = True)
    return render(request, 'taskmanager/dashboard.html', locals())




# ***************************************************************************
#  CALENDAR
# ***************************************************************************

@login_required(login_url = 'connect')
def calendar(request):
    current_user = User.objects.get(id = request.user.id)
    involved_projects = Project.objects.filter(members = current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks = Task.objects.filter(user = current_user, project = project).order_by('start_date')
        tasks_list = [dict(
            project_id = task.project.id,
            name = task.name,
            start = int(format(task.start_date, 'U'))*1000,
            end = int(format(task.due_date, 'U'))*1000
            ) for task in tasks]

        tasks_by_project_data = dict(project = project.name , tasks = tasks_list)
        tasks_by_project.append(tasks_by_project_data)

    tasks_by_project = json.dumps(tasks_by_project);
    return render(request, 'taskmanager/calendar.html', locals())
