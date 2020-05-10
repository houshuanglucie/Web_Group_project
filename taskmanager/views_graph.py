from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.utils.text import Truncator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

import datetime
import json

from .forms import LoginForm, ProjectForm, CommentForm, ProjectForm, TaskForm
from .models import Project, Status, Comment, Task, Category, Subtask
from .models import Verb, Trace

def print_json(data):
    print(json.dumps(data, indent = 1))

@login_required(login_url = 'connect')
def graphs(request):
    return render(request, 'taskmanager/graphs/graphs.html', locals())


# ***************************************************************************
#  GANTT
# ***************************************************************************

@login_required(login_url = 'connect')
def dashboard(request):
    # Juste une vue de taches de l'user par projets
    # C'était pour tenter une aggrégation des taches par projet (comme avec ElasticSearch),
    # mais pas réussi à le faire en une ligne...
    current_user = User.objects.get(id = request.user.id)
    involved_projects = Project.objects.filter(members = current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks_by_proj_data = dict(project = project, tasks = Task.objects.filter(user = current_user, project = project))
        tasks_by_project.append(tasks_by_proj_data)


    return render(request, 'taskmanager/graphs/dashboard.html', locals())

# ***************************************************************************
#  GANTT
# ***************************************************************************

@login_required(login_url = 'connect')
def gantt(request):
    # Juste pour envoyer une aggrégations de taches par projet a javascript ie :
    # tasks_by_project = list({
    #   project : nom_du_projet
    #   tasks : list({
    #       project_name : nom_du_projet_parent
    #       project_id : id_du_projet_parent
    #       name : nom_de_la_tache
    #       id_task : id_de_la_tache
    #       start : timestamp_unix_du_start_date_en_MILLISECONDES
    #       end : timestamp_unix_du_due_date_en_MILLISECONDES
    #   })
    #})
    current_user = User.objects.get(id = request.user.id)
    involved_projects = Project.objects.filter(members = current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks = Task.objects.filter(user = current_user, project = project).order_by('start_date')
        tasks_list = [dict(
            project_name = task.project.name,
            project_id = task.project.id,
            name = task.name,
            id_task = task.id,
            start = int(format(task.start_date, 'U'))*1000,
            end = int(format(task.due_date, 'U'))*1000
            ) for task in tasks]

        tasks_by_project_data = dict(project = project.name , tasks = tasks_list)
        tasks_by_project.append(tasks_by_project_data)

    tasks_by_project = json.dumps(tasks_by_project)
    return render(request, 'taskmanager/graphs/gantt.html', locals())



# ***************************************************************************
#  BURNDOWN CHART
# ***************************************************************************

@login_required(login_url = 'connect')
def burndown(request):
    involved_projects = Project.objects.filter(members = request.user)

    info_projects = []

    for project in involved_projects:
        tasks = Task.objects.filter(project = project)
        tasks_data = []
        for task in tasks:
            tasks_data.append(dict(
                name = task.name,
                shorten_name = Truncator(task.name).chars(20),
                start_date = int(format(task.start_date, 'U'))*1000,
                due_date = int(format(task.due_date, 'U'))*1000
            ))
        info_projects.append(dict(
            id_project = project.id,
            name_project = project.name,
            tasks_data = tasks_data
        ))

    info_projects = json.dumps(info_projects)

    return render(request, 'taskmanager/graphs/burndown.html', locals())


# ***************************************************************************
#  RADAR TASK
# ***************************************************************************

@login_required(login_url = 'connect')
def radartask(request):
    involved_projects = Project.objects.filter(members = request.user)

    info_project = []

    for project in involved_projects:
        members = project.members.all()
        member_data = []
        for member in members:
            count_task = Task.objects.filter(project = project).filter(user = member).count()
            member_data.append(dict(name = member.username, count = count_task))
        info_project.append(dict(
            name = project.name,
            id = project.id,
            members = member_data
        ))

    info_project = json.dumps(info_project)
    return render(request, 'taskmanager/graphs/radartask.html', locals())


# ***************************************************************************
#  RADAR ACTIVITY
# ***************************************************************************

@login_required(login_url = 'connect')
def radaractivity(request):

    involved_projects = Project.objects.filter(members = request.user)

    if(request.POST.get('range') and request.POST.get('range') == "global"):
        traces_sent = []
        for project in involved_projects:
            traces_sent.append(dict(
                axis = project.name,
                count = Trace.objects.filter(actor = request.user, object_project = project).count()
            ))

        return JsonResponse({'traces' : traces_sent, 'title' : "Vue globale"}, safe = False, status=200)

    elif(request.POST.get('range') and request.POST.get('range') == "project"):
        project_id = int(request.POST.get('project_id'))
        project = Project.objects.get(id = project_id)
        traces_sent = []

        for verb in Verb.objects.all():
            traces_sent.append(dict(
                axis = verb.verb,
                count = Trace.objects.filter(actor = request.user, object_project = project, verb = verb).count()
            ))

        return JsonResponse({'traces' : traces_sent, 'title' : project.name}, safe = False, status=200)

    return render(request, 'taskmanager/graphs/radaractivity.html', locals())


# ***************************************************************************
#  MANAGE APPLICATION
# ***************************************************************************
@login_required(login_url = 'connect')
def manageapp(request):
    if not request.user.is_superuser:
        return HttpResponse("Vous n'êtes pas autorisé.")

    nodes = []
    for user in User.objects.all():
        count = Trace.objects.filter(actor = user).count()
        nodes.append(dict(
            id = user.id,
            title = user.username + "<br>" + str(count) + " trace(s)",
            value = count,
            color = "rgb(150,150,150)",
            border = "rgb(100,100,100)"
        ))
    nodes = json.dumps(nodes)


    edges = []

    user_list = [user for user in User.objects.all()]
    for i in range(len(user_list)):
        user1 = user_list[i]
        for j in range(i+1, len(user_list)):
            user2 = user_list[j]
            count = Project.objects.filter(members = user1).filter(members = user2).count()
            if(count != 0):
                edges.append({
                    'from' : user1.id,
                    'to' : user2.id,
                    'value' : count,
                    'title' : str(count) + " projet(s) en commun",
                    'color' : "rgb(150,150,150)"
                })

    return render(request, 'taskmanager/graphs/manageapp.html', locals())
