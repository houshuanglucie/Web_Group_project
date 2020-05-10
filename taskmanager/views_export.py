import django.apps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files import File
from django.core import serializers

import csv

from .models import Project, Status, Comment, Task, Category, Subtask

@login_required(login_url='connect')
def export_xml(request):
    models = django.apps.apps.get_models('taskmanager')
    for model in models:
        data = serializers.serialize("xml", model.objects.all())
    response = HttpResponse(data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="models.xls"'
    return response


@login_required(login_url='connect')
def export_csv(request):
    current_user = User.objects.get(id=request.user.id)
    projects_list = Project.objects.filter(Q(members=current_user) | Q(public="PU")).distinct()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename= "Vos_projects.csv" '
    writer = csv.writer(response)
    writer.writerow(['Projet', 'Membres', 'Partage'])

    for project in projects_list:
        members = []
        for member in project.members.all():
            members.append(member.first_name + ' ' + member.last_name)
        writer.writerow([project.name, writer.writerow(members), project.public])

    return response
