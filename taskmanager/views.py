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
from django.db import models
from .forms import LoginForm, ProjectForm, CommentForm, ProjectForm, TaskForm, CompletedForm
from .models import Project, Status, Comment, Task, Category, Subtask
from .models import Verb, Trace

import datetime
import json


# =============== Page d'accueil =================
@login_required(login_url='connect')
def home(request):
    try:  # Si c'est la premiere fois qu'on lance la page et donc que ce champ n'existe pas
        if request.session['just_log']:  # Pour afficher un toast
            new_log = True
        else:
            new_log = False
    except:
        new_log = False
    request.session['just_log'] = False  # Pour ne pas reafficher le toast si on refresh la page

    return render(request, 'taskmanager/home.html', locals())


# ***************************************************************************
#  USER AUTHENTIFICATION
# ***************************************************************************

# =============== Page de redirection vers l'accueil =================
@login_required(login_url='connect')
def redirect_home(request):
    return redirect('home')


# =============== Page de connexion vue manuelle =================
'''
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
'''


# =============== Page de connexion vue générique =================
# Mais je suis pas convaincu de l'utilité des vues génériques...
# Ca prend plus de lignes de codes, et je ne trouve pas d'autre moyen que d'utiliser les request.session
# pour ce que je souhaite faire, mais vu que c'est demandé....
class LoginPage(FormView):
    template_name = "taskmanager/connect_gen.html"
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(LoginPage, self).get_context_data(**kwargs)
        try:
            context['error'] = self.request.session['error']  # Pour afficher le toast d'échec sur la page de connexion
        except KeyError:
            context['error'] = False

        self.request.session['error'] = False
        return context

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            self.request.session['just_log'] = True  # Pour afficher le toast sur la page d'accueil
            return redirect('home')
        else:
            # Si on a echec de la connexion, on revient sur la meme page en precisant qu'on vient d'échouer
            # pour ajouter un toast a la page (cf le try dans get_context_data)
            self.request.session['error'] = True
            return redirect('connect')


# =============== "Page" de deconnextion =================
# On redirige directement vers la page de connexion
@login_required(login_url='connect')
def disconnect(request):
    logout(request)
    return redirect('connect')


# ***************************************************************************
#  PROJECTS MANAGER
# ***************************************************************************

# =============== Page de vue de mes projets  =================
@login_required(login_url='connect')
def projects(request):
    current_user = User.objects.get(id=request.user.id)
    projects_list = Project.objects.filter(
        Q(members=current_user) | Q(public="PU")).distinct()  # projects de l'user OU les projets publics

    if (request.session.get('new_delete') != None):
        # Quand on arrive de la page manageproject et qu'on vient de supprimer un projet
        deleted_project = request.session.get('new_delete')
        request.session['new_delete'] = None
        show_toast = True
    else:
        deleted_project = None
        show_toast = False

    # On va calculer l'avancement global du projet
    for p in projects_list :
        a=0
        k=0
        for t in Task.objects.filter(project__id=p.id):
            a+=t.completed
            k+=1
        if(k>0):
            p.completed = int(a/k) # C'est la moyenne des avancements des tâches du projet

    return render(request, 'taskmanager/projects.html', locals())


# =============== Page de vue d'un projet =================
@login_required(login_url='connect')
def focus_project(request, id):
    # id : Id du projet sur lequel on se concentre
    project = Project.objects.get(id=id)
    tasks = Task.objects.filter(project__id=id).order_by('priority', '-due_date')

    # Si on vient de supprimer une tache (on arrive de la page managetask), pour qu'on ait un toast qui apparaisse
    if (request.session.get('new_delete') != None):
        deleted_task = request.session.get('new_delete')
        request.session['new_delete'] = None
        show_toast = True
    else:
        deleted_project = None
        show_toast = False

    return render(request, 'taskmanager/focus_project.html', locals())


# =============== Page de création d'un nouveau projet =================
# A cause du drag & drop, je ne peux pas utiliser le remplissage des forms normalement
# vu que le champ membres n'est pas un champ "normal". Je passe par de l'asynchrone avec
# ajax et du javascript
@login_required(login_url='connect')
def newproject(request):
    members = User.objects.all()
    members_of_project = []  # Ne sert a rien ici, juste que cette variable existe dans le template (utile dans manageproject)

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            list_members = request.POST.getlist('members[]')
            if list_members == []:
                # On envoie tout de suite a ajax/js un message qui dit que y a une erreur bad request
                return JsonResponse({"error": "No members"}, status=400)

            name = form.cleaned_data['name']
            project = Project(name=name)

            # Verification de l'aspect public ou privé
            if (request.POST.get("publicCheck") and request.POST.get("publicCheck") == 'on'):
                project.public = "PU"
            else:
                project.public = "PR"
            project.save()

            # Ajout des membres
            for member in list_members:
                project.members.add(User.objects.get(username=member))
            project.save()

            # Création d'une trace
            vb = Verb.objects.get(alias = "AddPr")
            new_trace = Trace(actor = request.user, object_project = project, verb = vb)
            new_trace.save()

            # On répond à Ajax qui va se charger d'afficher le toast
            return JsonResponse({"state": "ok", "name": name}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    else:
        form = ProjectForm()

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type="ADD")

    return render(request, 'taskmanager/formproject.html', locals())


# ***************************************************************************
#  TASKS MANAGER
# ***************************************************************************

# =============== Page de modification/suppression d'un projet =================
@login_required(login_url='connect')
def manageproject(request, id):
    # id : Id du projet qu'on veut modifier
    project = Project.objects.get(id=id)

    defaults = {'name': project.name}  # prepopulationner les champs
    members = []
    members_of_project = []

    # On divise les membres du projet et les non-membres pour les mettre dans
    # la bonne colonne avec du javascript (toujours a cause du drag & drop)
    for m in User.objects.all():
        if m in project.members.all():
            members_of_project.append(m)
        else:
            members.append(m)

    if request.method == 'POST':
        form = ProjectForm(request.POST, initial=defaults)

        if form.is_valid():
            # Si on a appuye sur le bouton delete, on supprimer le projet et on lui repond que tout va bien
            # Javascript va nous rediriger ensuite
            if (request.POST.get('action') and request.POST.get('action') == 'delete'):
                request.session['new_delete'] = project.name
                project.delete()
                return JsonResponse({"state": "ok"}, status=200)

            # Sinon, on modifie le projet
            elif (request.POST.get('action') and request.POST.get('action') == 'save'):
                list_members = request.POST.getlist('members[]')

                if list_members == []:
                    return JsonResponse({"error": "No members"}, status=400)

                project.name = form.cleaned_data['name']

                # Verification de l'aspect public ou privé
                if (request.POST.get("publicCheck") and request.POST.get("publicCheck") == 'on'):
                    project.public = "PU"
                else:
                    project.public = "PR"
                project.save()

                # MaJ des membres
                # Plus facile de tout supprimer et réinitialiser tous les membres plutot que de checker qui est nouveau
                project.members.clear()
                for member in list_members:
                    project.members.add(User.objects.get(username=member))

                project.save()

                # Création d'une trace
                vb = Verb.objects.get(alias = "MdfPr")
                new_trace = Trace(actor = request.user, object_project = project, verb = vb)
                new_trace.save()

                # On répond à Ajax qui va se charger d'afficher le toast
                return JsonResponse({"state": "ok", "name": project.name}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
    else:
        form = ProjectForm(initial=defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type="MODIFY")

    return render(request, 'taskmanager/formproject.html', locals())


# =============== Page de vue d'une tache =================
@login_required(login_url='connect')
def focus_task(request, id):
    # id : Id de la tache qu'on regarde
    task = Task.objects.get(id=id)
    comments = task.comments.all().order_by('-submit_time')

    subtasks = Subtask.objects.filter(task=task).order_by("id")

    # Si on vient de modifier une tache, pour qu'on ait un toast qui apparaisse
    if (request.session.get('new_modify') != None):
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

    # Gestion des commentaires (du journal)
    form_comment = CommentForm(request.POST or None)

    if form_comment.is_valid():
        new_comment = Comment(user=request.user, content=form_comment.cleaned_data['content'])
        new_comment.save()
        task.comments.add(new_comment)
        task.save()

        # Création d'une trace
        vb = Verb.objects.get(alias = "AddCm")
        new_trace = Trace(actor = request.user, object_project = task.project, object_task = task, verb = vb)
        new_trace.save()

    if task.completed<33:
        color="red"
    if task.completed>=33 and task.completed<66:
        color="orange"
    if task.completed >=66 :
        color="green"
    return render(request, 'taskmanager/focus_task.html', locals())


# =============== Validation de la création/modification d'une tache =================
# Pas possible de le faire comme un clean parce que y a du javascript qui vient tout chambouler.
# Du moins, je n'en ai pas l'impression
@login_required(login_url='connect')
def validate_task_data(request, form, project, action, task=None):
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

    if (action == "ADD"):
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
    if ('new_category' in request.POST and request.POST['new_category'] != '' and request.POST['category'] != ''):
        # Si l'user a choisi une categorie ET a aussi tapé une catégorie, on lui dit que c'est un etre indécis
        added = False
        error_category = True
        return added, error_category, None
    elif ('new_category' in request.POST and request.POST['new_category'] != '' and request.POST['category'] == ''):
        # S'il n'a que tapé, on crée une nouvelle catégorie
        # En termes de robustesse, j'aurais pu vérifier que la catégorie n'existait pas déjà, mais sinon, il faudrait faire un
        # message d'erreur, etc... bon.
        new_category = Category(name=request.POST['new_category'])
        new_category.save()
        task.category = new_category
    else:
        # S'il n'a que choisi dans les categories existantes
        task.category = form.cleaned_data['category']

    task.save()

    # Subtasks : pas un champ de task, mais dépend quand meme de task
    if (action == "ADD"):
        if ('new_subtask' in request.POST):
            # Si nouvelle sous-taches
            for subtask in request.POST.getlist('new_subtask'):
                if (subtask != ''):
                    new_subtask = Subtask(task=task, name=subtask)
                    new_subtask.save()
                # Si la sous tache est vide, on ne crée rien

    elif (action == "MODIFY"):
        former_subtasks = Subtask.objects.filter(task=task)

        if ('new_subtask' in request.POST):
            for subtask in request.POST.getlist('new_subtask'):
                if (subtask != ''):
                    if (former_subtasks.filter(name=subtask).count() == 1):
                        continue  # La subtask dans le formulaire était deja dans les anciennes subtask
                    else:  # Sinon, a priori, le count = 0, alors on cree la nouvelle subtask
                        new_subtask = Subtask(task=task, name=subtask)
                        new_subtask.save()
            for subtask in former_subtasks:
                # Pour tous les anciens subtasks qui ne sont plus dans le POST, (ie l'user les a supprimés),
                # alors on les supprime
                if subtask.name not in request.POST.getlist('new_subtask'):
                    subtask.delete()
        else:
            for subtask in former_subtasks:
                subtask.delete()

    return added, error_category, task


# =============== Page de création de tâche =================
@login_required(login_url='connect')
def newtask(request, id_project):
    # id_project : c'est clair je pense...
    added = False  # pour le toast de confirmation
    error_category = False  # pour le toast d'erreur d'utilisateur indécis

    project = Project.objects.get(id=id_project)
    defaults = {'status': Status.objects.all()[0], 'project': project}  # on coche au moins une case dans status
    # et on met project pour le __init__ du form, pour qu'on choisisse les bons membres a mettre dans le tag <select>

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial=defaults)
        if form.is_valid():
            added, error_category, new_task = validate_task_data(request, form, project, "ADD")

            # Création d'une trace
            vb = Verb.objects.get(alias = "AddTk")
            new_trace = Trace(actor = request.user, object_project = new_task.project, object_task = new_task, verb = vb)
            new_trace.save()
    else:
        form = TaskForm(initial=defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type="ADD")
    start_date_format = due_date_format = ""

    return render(request, 'taskmanager/formtask.html', locals())


# =============== Page de modification/suppression d'une tache =================
@login_required(login_url='connect')
def managetask(request, id):
    # id : Id de la tache qu'on veut modifier
    added = False  # pour le toast de confirmation
    error_category = False  # pour le toast d'erreur d'utilisateur indécis

    # On prepopulationne les champs
    task = Task.objects.get(id=id)
    project = task.project

    start_date_format = task.start_date.strftime("%d/%m/%Y %H:%M")
    due_date_format = task.due_date.strftime("%d/%m/%Y %H:%M")


    subtasks = Subtask.objects.filter(task=task).order_by("id")

    subtask_list = [subtask.name for subtask in subtasks]
    subtask_list = json.dumps(subtask_list)

    defaults = {'name': task.name,
                'description': task.description,
                'user': task.user,
                'priority': task.priority,
                'status': task.status,
                'category': task.category,
                'attachment': task.attachment,
                'project': project}

    if request.method == 'POST':
        form = TaskForm(request.POST or None, request.FILES, initial=defaults)
        if form.is_valid():
            if ('delete' in request.POST):
                request.session[
                    'new_delete'] = task.name  # pour afficher un toast quand on retournera sur focus_project
                task.delete()
                return redirect('focus_project', id=task.project.id)
            elif ('save' in request.POST):
                added, error_category, task = validate_task_data(request, form, task.project, "MODIFY", task)

                if(not error_category):

                    # Création d'une trace
                    vb = Verb.objects.get(alias = "MdfTk")
                    new_trace = Trace(actor = request.user, object_project = task.project, object_task = task, verb = vb)
                    new_trace.save()

                    request.session['new_modify'] = task.name # pour afficher un toast quand on retournera sur focus_task
                    return redirect('focus_task', id = task.id)

    else:
        form = TaskForm(initial=defaults)

    # parce qu'on utilise le meme template, a 2/3 choses differentes...
    particular = dict(type="MODIFY")
    return render(request, 'taskmanager/formtask.html', locals())


@login_required(login_url='connect')
def dashboard(request):
    # Juste une vue de taches de l'user par projets
    # C'était pour tenter une aggrégation des taches par projet (comme avec ElasticSearch),
    # mais pas réussi à le faire en une ligne...
    current_user = User.objects.get(id=request.user.id)
    involved_projects = Project.objects.filter(members=current_user)
    tasks_by_project = []
    for project in involved_projects:
        tasks_by_proj_data = dict(project=project, tasks=Task.objects.filter(user=current_user, project=project))
        tasks_by_project.append(tasks_by_proj_data)

    return render(request, 'taskmanager/dashboard.html', locals())


# ***************************************************************************
#  Filtrage et tri des task
# ***************************************************************************





# ============== Filtrage et de tri des taches =================
@login_required(login_url='connect')
def task_filter(request):

    # Quand le formulaire de filtre est soumis, le "click" devient "True",
    # utilisé pour afficher les résultats du filtre dans task_filter.html
    click = False

    # Obtenir les listes des menus déroulants dans le formulaire de filtre
    current_user = User.objects.get(id=request.user.id)
    project_list = Project.objects.filter(Q(members=current_user) | Q(public="PU")).distinct().values('id', 'name')  # projects de l'user OU les projets publics
    user_list = User.objects.all().values('id', 'first_name', 'last_name')
    status_list = Status.objects.all().values('id', 'how')

    if request.method == 'POST':

        # Quand le clic devient "True", le frontal affiche le résultat du filtrage
        click = True

        # Récupérer le paramètre utilisé pour le tri
        sorter = request.POST.get('sorter')
        if sorter == "default":
            sorter = "priority"

        order = request.POST.get('order')
        if order == "descent":
            sorter = '-' + str(sorter)  # Trier dans l'ordre inverse

        # Récupérer les paramètres de filtrage sélectionnés par le frontal
        project_selected = request.POST.get('project_selected')
        assignee_selected = request.POST.get('assignee_selected')
        status_inc_exc = request.POST.get('status_inc_exc')
        status_selected_list = request.POST.getlist('status_selected')
        start_before_after = request.POST.get('start_before_after')
        start_date_selected = request.POST.get('start_date_selected')
        due_before_after = request.POST.get('due_before_after')
        due_date_selected = request.POST.get('due_date_selected')

        filter_dict = dict()

        # Filtrer par projet et responsable(assignee)
        if project_selected != "All":
            filter_dict['project'] = get_object_or_404(Project, id=project_selected)
        if assignee_selected != "All":
            if assignee_selected == "moi":
                filter_dict['user'] = get_object_or_404(User, id=current_user.id)
            else:
                filter_dict['user'] = get_object_or_404(User, id=assignee_selected)

        task_list = Task.objects.filter(**filter_dict).order_by(sorter)

        # Filtrer par date de début (avant ou après)
        if start_before_after == "Before" and start_date_selected != "":
            task_list = task_list.filter(start_date__lte=start_date_selected).order_by(sorter)
        elif start_before_after == "After" and start_date_selected != "":
            task_list = task_list.filter(start_date__gte=start_date_selected).order_by(sorter)
        else:
            task_list = task_list.order_by(sorter)

        # Filtrer par date d'écheance (avant ou après)
        if due_before_after == "Before" and due_date_selected != "":
            task_list = task_list.filter(due_date__lte=due_date_selected).order_by(sorter)
        elif due_before_after == "After" and due_date_selected != "":
            task_list = task_list.filter(due_date__gte=due_date_selected).order_by(sorter)
        else:
            task_list = task_list.order_by(sorter)

        # Filtrer par status(inclus ou exclu)
        if status_inc_exc == "include":
            if status_selected_list:
                status_exc_list = status_list  # Initialiser la liste des statuts à exclure
                for status_selected in status_selected_list:
                    status_exc_list = status_exc_list.exclude(id=status_selected)
                for status_exc in status_exc_list:
                    task_list = task_list.exclude(status__id=status_exc['id']).order_by(sorter)
            else:
                task_list = task_list.order_by(sorter)

        elif status_inc_exc == "exclude":
            if status_selected_list:
                for status_selected in status_selected_list:
                    task_list = task_list.exclude(status__id=status_selected).order_by(sorter)
            else:
                task_list = Task.objects.none()

        return render(request, 'taskmanager/task_filter.html', locals())

    else:
        return render(request, 'taskmanager/task_filter.html', locals())


# --- Page d'affichage des projets d'un utilisateur ainsi que des autres membres ---#
def projects_members(request):
    current_user = User.objects.get(id=request.user.id)  # oN R2CUP7RE L4UTILISATEUR CONNECT2
    proj = []  # Liste des projets dont l'utilisateur fait partie

    for p in Project.objects.all():
        Present = False
        memb = p.members.all()
        for m in memb:
            if m.id == current_user.id:  # Alors l'utilisateur fait partie de ce projet
                Present = True
        if Present:
            proj += [p]  # On ajoute le projet puisque l'utilisateur en fait partie

    return render(request, 'taskmanager/list_members_project.html/', locals())


def list_tasks(request):
    empty = False
    tasks = Task.objects.filter(user__id=request.user.id)
    if (len(tasks) == 0):
        empty = True
    return render(request, 'taskmanager/list_tasks.html', locals())


def finished_tasks(request):
    empty_f = False
    tasks = Task.objects.filter(user=request.user).filter(status=4)
    if (len(tasks) == 0):
        empty_f = True
    return render(request, 'taskmanager/list_tasks.html', locals())


def distinct_tasks(request, ide):
    user_empty = False
    others_empty = False
    project = Project.objects.get(id=ide)
    user_tasks = Task.objects.filter(project__id=ide).filter(user__id=request.user.id)
    if (len(user_tasks) == 0):
        user_empty = True
    print(user_tasks)
    othertasks = Task.objects.filter(project__id=ide).exclude(user__id=request.user.id)
    if (len(othertasks) == 0):
        others_empty = True
    return render(request, 'taskmanager/distinct_tasks.html', locals())


def activities(request, ide):


    tasks = Task.objects.filter(project__id=ide)



    ordered_tasks = tasks.order_by('-comments') # On trie les commentaires
    ordered_comments = []
    list_tasks = []
    for t in ordered_tasks: # On va maintenant ne garder que le commentaire le plus récent de chaque tâche
        present = False
        for l in list_tasks:
            if(l.name==t.name):
                present = True
        if not present :
            if(len(t.comments.all())>0):
                    ordered_comments += [t.comments.all()[len(t.comments.all())-1]] # On récupère aussi les commentaires triés pour les afficher
            else:
                ordered_comments += ["empty"]
            list_tasks += [t]

    return render(request, 'taskmanager/activities.html', locals())


def ModifyAvancement(request,id):
    task = Task.objects.get(id=id)
    form = CompletedForm(request.POST or None)
    if form.is_valid():
        task.completed = form.cleaned_data['completed']
        # L'avancement de la tâche influe sur son statut
        if(task.completed==100):
            task.status=Status(4)
        if(task.completed<100 and task.completed>0):
            task.status=Status(3)
        if(task.completed==0):
            task.status=Status(1)

        task.save()

        # Création d'une trace (pour les graphs)
        vb = Verb.objects.get(alias = "MdfAv")
        new_trace = Trace(actor = request.user, object_project = task.project, object_task = task, verb = vb, extension_integer = task.completed)
        new_trace.save()

        return redirect('focus_task',id=id)
    return render(request,'taskmanager/avancement.html',locals())
