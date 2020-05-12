import django.apps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

import csv

from .models import Project, Status, Comment, Task, Category, Subtask


@login_required(login_url='connect')
def export_xml(request,id):
    models = django.apps.apps.get_models()
    model = models[id]
    data = serializers.serialize("xml", model.objects.all())
    response = HttpResponse(data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="export.xml"'
    return response


@login_required(login_url='connect')
def export_json(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    data = serializers.serialize("json", model.objects.all())
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename= "export.json"'
    return response


@login_required(login_url='connect')
def export_csv(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "export.csv"'
    list_fields = model._meta.get_fields()
    names = []
    if id==6:
        list_items = model.objects.all().values_list('id', 'name', 'members', 'public')
        names = ['id','name','member','public']
    else:
        list_items = model.objects.all().values_list()
        list_fields = model._meta.get_fields()
        for field in list_fields:
            names.append(field.name)
    writer = csv.writer(response)
    writer.writerow(names)
    for item in list_items:
        writer.writerow(item)
    return response
