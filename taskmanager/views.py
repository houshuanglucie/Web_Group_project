from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Project, Status, Comment, Task

@login_required(login_url = 'connect')
def home(request):
    return render(request, 'taskmanager/home.html', locals())

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
            else:
                error = True
    else:
        form = LoginForm()

    return render(request, 'taskmanager/connect.html', locals())

@login_required(login_url = 'connect')
def disconnect(request):
    logout(request)
    return redirect('connect')


@login_required(login_url = 'connect')
def projects(request):
    projects_list = Project.objects.all() # TODO A remplacer par ou contains
    return render(request, 'taskmanager/projects.html', locals())


@login_required(login_url = 'connect')
def focus_project(request, id):
    project = Project.objects.get(id = id)
    tasks = Task.objects.filter(project__id = id)
    return render(request, 'taskmanager/focus_project.html', locals())
