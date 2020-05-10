from taskmanager.models import Project, Status, Comment, Task, Category, Subtask
from django.contrib.auth import get_user_model

UserModel = get_user_model()


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
        else:
            print('user{} already exists'.format(i))
    print("Useless users created")



def delete_users():
    global UserModel
    useless_users = UserModel.objects.filter(username__startswith = "user")
    for user in useless_users:
        user.delete()
    print("Useless users deleted")



def create_projects():
    import random as rd
    from taskmanager.models import Project
    N_CREATED = 30
    N_MEMBERS_MAX = 10

    global UserModel
    all_users = UserModel.objects.all()
    for i in range(N_CREATED):
        number_members = rd.randint(1, N_MEMBERS_MAX)
        chosen_members_index = rd.sample(range(0, all_users.count()), number_members)

        project = Project(name = 'Project{}'.format(i))
        project.save()

        for index in chosen_members_index:
            project.members.add(all_users[index])

        project.save()
    print("Useless projects created")



def delete_projects():
    from taskmanager.models import Project

    useless_projects = Project.objects.filter(name__startswith = "Project")
    for project in useless_projects:
        project.delete()

    print("Useless projects deleted")


"""
    (1) Create users
    (2) Delete users
    (3) Create projects
    (4) Delete projects
"""

i = 3

if (i == 1):
    create_users()
elif (i == 2):
    delete_users()
elif (i == 3):
    create_projects()
elif (i == 4):
    delete_projects()
