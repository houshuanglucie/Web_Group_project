from taskmanager.models import Project, Status, Comment, Task, Category, Subtask
from django.contrib.auth import get_user_model
from random import randrange
from datetime import timedelta

UserModel = get_user_model()

"""
    (1) Create users
      (2) Delete users
    (3) Create projects
      (4) Delete projects
    (5) Create tasks
      (6) Delete tasks
    (7) Create journal
      (8) Delete journal
      (9) Delete traces
"""

i = "5"




# =========================================================================================
# CREATION D'USERS
# =========================================================================================
def create_users():
    global UserModel
    N_CREATED = 30

    for i in range(N_CREATED):
        if not UserModel.objects.filter(username = 'user{}'.format(i)).exists():
            user = UserModel.objects.create_user('user{}'.format(i), password='bar')
            user.first_name = 'User{}'.format(i)
            user.last_name = 'User{}'.format(i)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            print(user.username + " created")
        else:
            print('user{} already exists'.format(i))
    print("=== Useless users created ===")



def delete_users():
    global UserModel
    useless_users = UserModel.objects.filter(username__startswith = "user")
    for user in useless_users:
        print(user.username + " deleted")
        user.delete()
    print("=== Useless users deleted ===")



# =========================================================================================
# CREATION DE PROJETS
# =========================================================================================
def create_projects():
    import random as rd
    from taskmanager.models import Project
    global UserModel
    N_CREATED = 30
    N_MEMBERS_MAX = 7

    all_users = UserModel.objects.all()
    for i in range(N_CREATED):
        number_members = rd.randint(1, N_MEMBERS_MAX)
        chosen_members_index = rd.sample(range(0, all_users.count()), number_members)

        project = Project(name = 'Project{}'.format(i))
        project.save()

        for index in chosen_members_index:
            project.members.add(all_users[index])

        project.save()
        print(project.name + " created")
    print("=== Useless projects created ===")



def delete_projects():
    from taskmanager.models import Project

    useless_projects = Project.objects.filter(name__startswith = "Project")
    for project in useless_projects:
        print(project.name + " deleted")
        project.delete()

    print("=== Useless projects deleted ===")




# =========================================================================================
# CREATION DE TACHES
# =========================================================================================
def create_tasks():
    import random as rd
    import datetime
    from taskmanager.models import Project, Task, Status, Trace, Verb
    global UserModel

    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = rd.randrange(int_delta)
        return start + datetime.timedelta(seconds=random_second)


    N_CREATED = 60
    ALL_PROJECTS = Project.objects.all()
    N_PROJECTS = ALL_PROJECTS.count()
    START_DATE = datetime.datetime(2020, 5, 1, 0, 0, 0)
    END_DATE = datetime.datetime(2020, 8, 1, 0, 0, 0)

    for i in range(N_CREATED):
        project_selected = ALL_PROJECTS[rd.randint(0, N_PROJECTS-1)]
        # project_selected = ALL_PROJECTS

        n_members = project_selected.members.all().count()
        member_selected = project_selected.members.all()[rd.randint(0, n_members-1)]

        start_date = random_date(START_DATE, END_DATE)
        due_date = random_date(start_date, END_DATE)

        new_task = Task(
            project = project_selected,
            name = 'Task{}'.format(i),
            user = member_selected,
            start_date = start_date,
            due_date = due_date,
            priority = 1,
            status = Status.objects.all()[0],
        )

        new_task.save()

        # Création d'une trace
        vb = Verb.objects.get(alias = "AddTk")
        new_trace = Trace(
            alias = "Trace{}".format(i),
            actor = member_selected,
            object_project = project_selected,
            object_task = new_task,
            verb = vb
            )
        new_trace.save()

        print(new_task.name + " created + Trace for {}".format(member_selected))

    print("=== Useless tasks created ===")


def delete_tasks():
    from taskmanager.models import Task

    useless_tasks = Task.objects.filter(name__startswith = "Task")
    for task in useless_tasks:
        print(task.name + " deleted")
        task.delete()

    print("=== Useless tasks deleted ===")


# =========================================================================================
# CREATION DE DE COMMENTAIRES
# =========================================================================================
def create_com():
    import random as rd
    import datetime
    from taskmanager.models import Project, Task, Status, Trace, Verb, Comment
    global UserModel

    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = rd.randrange(int_delta)
        return start + datetime.timedelta(seconds=random_second)

    N_CREATED = 30
    ALL_TASKS = Task.objects.all()
    N_TASKS = ALL_TASKS.count()
    START_DATE = datetime.datetime(2020, 5, 1, 0, 0, 0)
    END_DATE = datetime.datetime(2020, 8, 1, 0, 0, 0)

    for i in range(N_CREATED):
        task_selected = ALL_TASKS[rd.randint(0, N_TASKS-1)]
        member_of_projects = task_selected.project.members.all()
        member_selected = member_of_projects[rd.randint(0, member_of_projects.count()-1)]

        submit_date = random_date(START_DATE, END_DATE)

        new_comment = Comment(
            user = member_selected,
            submit_time = submit_date,
            content = "Comment{}".format(i)
        )

        new_comment.save()
        task_selected.comments.add(new_comment)
        task_selected.save()

        vb = Verb.objects.get(alias = "AddCm")
        new_trace = Trace(
            alias = "Trace{}".format(i),
            actor = member_selected,
            object_project = task_selected.project,
            object_task = task_selected,
            verb = vb
            )
        new_trace.save()

        print( "Comment{} + Trace created for {}".format(i, member_selected))

    print("=== Useless comments created ===")


def delete_com():
    from taskmanager.models import Comment

    useless_comments = Comment.objects.filter(content__startswith = "Comment")
    for comment in useless_comments:
        print(comment.content + " deleted")
        comment.delete()

    print("=== Useless comments deleted ===")



# =========================================================================================
# SUPRRESSION DE TRACES
# =========================================================================================

def delete_traces():
    from taskmanager.models import Trace

    useless_traces = Trace.objects.filter(alias__startswith = "Trace")
    for trace in useless_traces:
        print(trace.alias + " deleted")
        trace.delete()

    print("=== Useless traces deleted ===")


if ("1" in i):
    create_users()
if ("2" in i):
    delete_users()
if ("3" in i):
    create_projects()
if ("4" in i):
    delete_projects()
if ("5" in i):
    create_tasks()
if ("6" in i):
    delete_tasks()
if ("7" in i):
    create_com()
if ("8" in i):
    delete_com()
if ("9" in i):
    delete_traces()
