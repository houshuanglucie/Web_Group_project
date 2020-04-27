from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, ProjectForm
from .models import Project, Status, Comment, Task

import datetime

# TODO Gerer la responsibite, ca va pas du tout la...

@login_required(login_url = 'connect')
def home(request):
    try:
        if request.session['just_log']: # To show a popup window
            new_log = True
        else:
            new_log = False
    except:
        new_log = False
    request.session['just_log'] = False

    return render(request, 'taskmanager/home.html', locals())


# ===========================================================================
#  USER AUTHENTIFICATION
# ===========================================================================
@login_required(login_url = 'connect')
def redirect_home(request):
    return redirect('home')


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

@login_required(login_url = 'connect')
def disconnect(request):
    logout(request)
    return redirect('connect')



# ===========================================================================
#  PROJECTS MANAGER
# ===========================================================================

@login_required(login_url = 'connect')
def projects(request):
    current_user = User.objects.get(id = request.user.id)
    projects_list = Project.objects.filter(members = current_user)
    projects_list = Project.objects.all()
    return render(request, 'taskmanager/projects.html', locals())


@login_required(login_url = 'connect')
def focus_project(request, id):
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project__id = id).order_by('priority', '-due_date')
    return render(request, 'taskmanager/focus_project.html', locals())


@login_required(login_url = 'connect')
def newproject(request):
    added = False
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        members = form.cleaned_data['members']
        new_project = Project(name = name)
        new_project.save()
        new_project.members.set(members)
        new_project.save()
        added = True
    return render(request, 'taskmanager/newproject.html', locals())


# ===========================================================================
#  TASKS MANAGER
# ===========================================================================

@login_required(login_url = 'connect')
def manageproject(request):
    added = False
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        members = form.cleaned_data['members']
        new_project = Project(name = name)
        new_project.save()
        new_project.members.set(members)
        new_project.save()
        added = True
    return render(request, 'taskmanager/newproject.html', locals())



@login_required(login_url = 'connect')
def focus_task(request, id):
    task = Task.objects.get(id = id)
    print(task.due_date.date() - datetime.datetime.now().date(), flush = True)
    return render(request, 'taskmanager/focus_task.html', locals())
