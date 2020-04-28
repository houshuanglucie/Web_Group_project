from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, NewProjectForm, CommentForm, ManageProjectForm, NewTaskForm
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

    if(request.session.get('new_delete') != None):
        deleted_project = request.session.get('new_delete')
        request.session['new_delete'] = None
        show_toast = True
    else:
        deleted_project = None
        show_toast = False
    return render(request, 'taskmanager/projects.html', locals())


@login_required(login_url = 'connect')
def focus_project(request, id):
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project__id = id).order_by('priority', '-due_date')
    return render(request, 'taskmanager/focus_project.html', locals())


@login_required(login_url = 'connect')
def newproject(request):
    added = False
    form = NewProjectForm(request.POST or None)
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
def manageproject(request, id):
    added = False
    project = Project.objects.get(id = id)

    defaults = {'name' : project.name}
    defaults['members'] = [m for m in project.members.all()]
    form = ManageProjectForm(request.POST or None, initial=defaults)

    if form.is_valid():
        if('delete' in request.POST):
            request.session['new_delete'] = project.name
            project.delete()
            return redirect('projects')
        elif('save' in request.POST):
            project.name = form.cleaned_data['name']
            project.members.set(form.cleaned_data['members'])
            project.save()
            added = True
    return render(request, 'taskmanager/manageproject.html', locals())



@login_required(login_url = 'connect')
def focus_task(request, id):
    task = Task.objects.get(id = id)
    comments = task.comments.all().order_by('-submit_time')
    form_comment = CommentForm(request.POST or None)

    if form_comment.is_valid():
        new_comment = Comment(user = request.user, content = form_comment.cleaned_data['content'])
        new_comment.save()
        task.comments.add(new_comment)
        task.save()
    return render(request, 'taskmanager/focus_task.html', locals())



@login_required(login_url = 'connect')
def newtask(request, id_project):
    added = False
    project = Project.objects.get(id = id_project)
    defaults = {'status' : Status.objects.all()[0]}
    form = NewTaskForm(request.POST or None, initial=defaults)

    if form.is_valid():
        added = True
        new_task = Task()
        new_task.project = project
        new_task.name = form.cleaned_data['name']
        new_task.description = form.cleaned_data['description']
        new_task.user = form.cleaned_data['user']
        new_task.start_date = form.cleaned_data['start_date']
        new_task.due_date = form.cleaned_data['due_date']
        new_task.priority = form.cleaned_data['priority']
        new_task.status = form.cleaned_data['status']
        new_task.save()
    return render(request, 'taskmanager/newtask.html', locals())



# TODO Calendrier https://alexpnt.github.io/2017/07/15/django-calendar/
# https://medium.com/@unionproject88/django-and-python-calendar-e647a8eccff6
# https://www.geeksforgeeks.org/python-calendar-module/
