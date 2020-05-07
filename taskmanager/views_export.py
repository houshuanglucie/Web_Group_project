from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

import csv

from .models import Project, Status, Comment, Task, Category, Subtask


@login_required(login_url='connect')
def export_csv(request):
    current_user = User.objects.get(id=request.user.id)
    projects_list = Project.objects.filter(Q(members=current_user) | Q(public="PU")).distinct()

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Projet', 'Membres', 'Partage'])

    for project in projects_list:
        members = []
        for member in project.members.all():
            members.append(member.first_name+' '+member.last_name)
        writer.writerow([project.name, members, project.public])
    response['Content-Disposition'] = 'attachement; filename= "projects.csv" '

    return response
