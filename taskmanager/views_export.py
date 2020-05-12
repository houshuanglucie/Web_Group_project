import django.apps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

import csv, xlwt

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

@login_required(login_url='connect')
def export_excel(request, id):
    models = django.apps.apps.get_models()
    model = models[id]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="model.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model.__class__.__name__)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    names = []
    if id==6:
        list_items = model.objects.all().values_list('id', 'name', 'members', 'public')
        names = ['id','name','member','public']
    else:
        list_items = model.objects.all().values_list()
        list_fields = model._meta.get_fields()
        for field in list_fields:
            names.append(field.name)

    for col_num in range(len(names)):
        ws.write(row_num,col_num, names[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in list_items:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
