from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

import datetime
import json

from .forms import LoginForm, ProjectForm, CommentForm, ProjectForm, TaskForm
from .models import Project, Status, Comment, Task, Category, Subtask


@login_required(login_url = 'connect')
def graphs(request):
    return render(request, 'taskmanager/graphs/graphs.html', locals())


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

    tasks_by_project = json.dumps(tasks_by_project);
    return render(request, 'taskmanager/graphs/gantt.html', locals())


# ***************************************************************************
#  DIAGRAMME D'ACTIVITE
# ***************************************************************************

@login_required(login_url = 'connect')
def activitydiag(request):
    return render(request, 'taskmanager/graphs/activitydiag.html', locals())


# ***************************************************************************
#  BURNDOWN CHART
# ***************************************************************************

@login_required(login_url = 'connect')
def burndown(request):
    return render(request, 'taskmanager/graphs/burndown.html', locals())


# ***************************************************************************
#  RADAR TASK
# ***************************************************************************

@login_required(login_url = 'connect')
def radartask(request):
    return render(request, 'taskmanager/graphs/radartask.html', locals())


# ***************************************************************************
#  RADAR ACTIVITY
# ***************************************************************************

@login_required(login_url = 'connect')
def radaractivity(request):
    return render(request, 'taskmanager/graphs/radaractivity.html', locals())
