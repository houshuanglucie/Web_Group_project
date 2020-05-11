import django.apps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers

import csv

from .models import Project, Status, Comment, Task, Category, Subtask


@login_required(login_url='connect')
def export_xml(request,id):
    models = django.apps.apps.get_models()
    model = models[id]
    data = serializers.serialize("xml", model.objects.all())
    response = HttpResponse(data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="models.xls"'
    return response


@login_required(login_url='connect')
def export_json(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    data = serializers.serialize("json", model.objects.all())
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename= "export.json"'
    return response
