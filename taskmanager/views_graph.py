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
import colorsys

from .forms import LoginForm, ProjectForm, CommentForm, ProjectForm, TaskForm
from .models import Project, Status, Comment, Task, Category, Subtask
from .models import Verb, Trace

def print_json(data):
    print(json.dumps(data, indent = 1))


# ***************************************************************************
#  PAGE D'ACCUEIL DES GRAPHES
# ***************************************************************************
@login_required(login_url = 'connect')
def graphs(request):
    return render(request, 'taskmanager/graphs/graphs.html', locals())


# ***************************************************************************
#  DASHBOARD
# ***************************************************************************

@login_required(login_url = 'connect')
def dashboard(request):

    # Pour la vue ddes taches par projet
    current_user = User.objects.get(id = request.user.id)
    involved_projects = Project.objects.filter(members = current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks_by_proj_data = dict(project = project, tasks = Task.objects.filter(user = current_user, project = project))
        tasks_by_project.append(tasks_by_proj_data)

    # Receptions AJAX pour les vues demandant d'autres graphs
    if request.POST.get('type_view') and request.POST.get('type_view') == "gantt":
        tasks_by_project = create_data_gantt(request)
        return JsonResponse({'tasks' : tasks_by_project}, safe = False, status=200)

    elif request.POST.get('type_view') and request.POST.get('type_view') == "burndown":
        info_projects = create_data_burndown(request)
        return JsonResponse({'info' : info_projects}, safe = False, status=200)

    elif request.POST.get('type_view') and request.POST.get('type_view') == "radartask":
        info_projects = create_data_radartask(request)
        return JsonResponse({'info' : info_projects}, safe = False, status=200)

    elif request.POST.get('type_view') and request.POST.get('type_view') == "radaractivity":
        traces_sent = create_data_radaractivity(request)
        return JsonResponse({'traces' : traces_sent}, safe = False, status=200)

    return render(request, 'taskmanager/graphs/dashboard.html', locals())

# ***************************************************************************
#  GANTT
# ***************************************************************************

# =============== Création des données pour Gantt =================
def create_data_gantt(request):
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


    return tasks_by_project


# =============== Page de Gantt =================
@login_required(login_url = 'connect')
def gantt(request):
    tasks_by_project = create_data_gantt(request)
    tasks_by_project = json.dumps(tasks_by_project)
    return render(request, 'taskmanager/graphs/gantt.html', locals())



# ***************************************************************************
#  BURNDOWN CHART
# ***************************************************************************
# =============== Création des données pour le burndown =================
def create_data_burndown(request):
    # info_project = list({
    #   id_project : id_du_projet,
    #   name_project : nom_du_projet,
    #   tasks_data = list({
    #       name : nom_de_la_tache
    #       shorten_name : nom_de_la_tache_tronquée
    #       start_date : date_de_debut_theorique
    #       due_date : date_de_fin_theorique
    #       list_traces : list({
    #           timestamp : quand_la_trace_de_modification_d_avancement_a_ete_ajoutee
    #           progress : avancement_entré
    #       })
    #   })
    # })

    involved_projects = Project.objects.filter(members = request.user)
    info_projects = []

    for project in involved_projects:
        tasks = Task.objects.filter(project = project).order_by('start_date')
        tasks_data = []

        for task in tasks:
            # Recherche de toutes les traces d'avancement concernant cette tache
            traces_progress = Trace.objects.filter(object_task = task, verb__alias = "MdfAv").order_by('timestamp')
            list_trace = []

            for trace in traces_progress:
                list_trace.append(dict(
                    timestamp = int(format(trace.timestamp, 'U'))*1000,
                    progress = trace.extension_integer
                ))

            # Ajout de toutes les info
            tasks_data.append(dict(
                name = task.name,
                shorten_name = Truncator(task.name).chars(20),
                start_date = int(format(task.start_date, 'U'))*1000,
                due_date = int(format(task.due_date, 'U'))*1000,
                progress_traces = list_trace
            ))
        info_projects.append(dict(
            id_project = project.id,
            name_project = project.name,
            tasks_data = tasks_data
        ))
    return info_projects

# =============== Page du burndown =================
@login_required(login_url = 'connect')
def burndown(request):
    involved_projects = Project.objects.filter(members = request.user)
    info_projects = create_data_burndown(request)
    info_projects = json.dumps(info_projects)

    return render(request, 'taskmanager/graphs/burndown.html', locals())


# ***************************************************************************
#  RADAR TASK
# ***************************************************************************
# =============== Création des données pour le radartask =================
def create_data_radartask(request):
    # info_project = list({
    #   name : nom_du_projet,
    #   id : id_du_projet,
    #   members = list({
    #       name : nom_du_membre
    #       count : nombre_de_tache_du_membre_dans_ce_projet
    #   })
    # })
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

    return info_project

# =============== Page du radartask =================
@login_required(login_url = 'connect')
def radartask(request):
    involved_projects = Project.objects.filter(members = request.user)
    info_project = create_data_radartask(request)
    info_project = json.dumps(info_project)
    return render(request, 'taskmanager/graphs/radartask.html', locals())


# ***************************************************************************
#  RADAR ACTIVITY
# ***************************************************************************
# =============== Création des données du radaractivity =================
# Juste pour le radar : nombre de traces laissees sur chaque projet
def create_data_radaractivity(request):
    # traces_sent = list({
    #   axis : nom_des_projets,
    #   count : nombre_de_traces_laissees_par_l_utilisateur_sur_ce_projet
    # })
    involved_projects = Project.objects.filter(members = request.user)
    traces_sent = []
    for project in involved_projects:
        traces_sent.append(dict(
            axis = project.name,
            count = Trace.objects.filter(actor = request.user, object_project = project).count()
        ))
    return traces_sent

# =============== Page du radaractivity =================
# Pour le radar individuel et le radar par projet (types de traces laissees projet)
# Pour le radar individuel : voir dessus
@login_required(login_url = 'connect')
def radaractivity(request):
    # Pour le radar par projet :
    # traces_sent = list({
    #   axis : verbe (type de trace),
    #   count : nombre_de_traces_laissees_par_l_utilisateur_sur_ce_projet_de_ce_type_la
    # })

    involved_projects = Project.objects.filter(members = request.user)

    if(request.POST.get('range') and request.POST.get('range') == "global"):
        traces_sent = create_data_radaractivity(request)
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
# Convertit Hue/Saturation/Value into R/G/B
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

# Retourne l'item count d'un dict
def getCount(d):
    return d['count']

# =============== Graphe d'activités sur l'application =================
@login_required(login_url = 'connect')
def manageapp(request):

    # Si ce n'est pas un super utilisateur, on lui renvoie une page HTML sans âme
    if not request.user.is_superuser:
        return HttpResponse("Vous n'êtes pas autorisé.")

    # *************** GRAPHE D'ACTIVITES *********************
    # *** NOEUDS ***
    # Qui sont les differents utilisateurs, et dont la taille du noeud est
    # pondérée par le nombre de traces laissées par l'user
    max_count = 0
    for user in User.objects.all():
        count = Trace.objects.filter(actor = user).count()
        if max_count < count:
            max_count = count


    nodes = []
    YELLOW_HUE = 107
    for user in User.objects.all():
        count_traces = Trace.objects.filter(actor = user).count()
        hue = 107/360 * (1 - count_traces/max_count)
        color = hsv2rgb(hue, 1, 0.5)
        count_project = Project.objects.filter(members = user).count()

        nodes.append(dict(
            id = user.id,
            title = "<b>{}<br>{} trace(s)<br>{} projet(s)</b>".format(user.username, count_traces, count_project),
            value = count_traces,
            color = "rgb{}".format(color),
            border = "rgb(100,100,100)"
        ))
    nodes = json.dumps(nodes)

    # *** ARETES ***
    # Largeurs pondérées par les differents projets entre utilisateurs
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
                    'title' : "<b>{} projet(s) en commun</b>".format(count),
                    'color' : "rgb(100,100,100)",
                    'length' : 50
                })

    # *************** UTILISATEURS LES PLUS ACTIFS *********************
    # Une simple classement des utilisateurs en fonction de leur nb de traces laissees
    users = User.objects.all()
    list_active_users = []
    for user in users:
        list_active_users.append(dict(
            username = user.username,
            count = Trace.objects.filter(actor = user).count()
        ))

    list_active_users.sort(key = getCount, reverse = True)



    return render(request, 'taskmanager/graphs/manageapp.html', locals())
