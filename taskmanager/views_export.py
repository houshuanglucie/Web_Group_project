import django.apps
from django.db.models import ManyToOneRel
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers

import csv, xlwt

from .models import Project, Status, Comment, Task, Category, Subtask


@login_required(login_url='connect')
def export_xml(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    filename = model.__name__ + '.xml'
    data = serializers.serialize("xml", model.objects.all())
    response = HttpResponse(data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


@login_required(login_url='connect')
def export_json(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    filename = model.__name__ + '.json'
    data = serializers.serialize("json", model.objects.all())
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
    return response


@login_required(login_url='connect')
def export_csv(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    filename = model.__name__ + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)

    writer = csv.writer(response)
    fields = model._meta.get_fields()
    fields_names = [field.name for field in fields]
    writer.writerow(fields_names)

    for item in model.objects.all():
        row = []
        for field in fields:
            name = field.name
            try:
                field_type = field.get_internal_type()
                if str(field_type) == 'ManyToManyField':
                    data = ''
                    list_keys = getattr(item, name)
                    for key in list_keys.all():
                        data += str(key.id)+', '
                    row.append(data)
                else:
                    data = str(getattr(item, name))
                    row.append(data)
            except:
                row.append(" ")
        writer.writerow(row)

    return response


@login_required(login_url='connect')
def export_excel(request, id):
    models = django.apps.apps.get_models()
    model = models[id]
    filename = model.__name__ + '.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    fields = model._meta.get_fields()
    fields_names = [field.name for field in fields]

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model.__name__)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    names = []

    list_items = model.objects.all().values_list()
    list_fields = model._meta.get_fields()
    for field in list_fields:
            names.append(field.name)

    for col_num in range(len(names)):
        ws.write(row_num, col_num, names[col_num], font_style)

    font_style = xlwt.XFStyle()

    for item in model.objects.all():
        row_num += 1
        col_num = 0
        row = []
        for field in fields:
            name = field.name
            try:
                field_type = field.get_internal_type()
                if str(field_type) == 'ManyToManyField':
                    data = ''
                    list_keys = getattr(item, name)
                    for key in list_keys.all():
                        data += str(key.id)+', '
                    ws.write(row_num, col_num, data, font_style)
                else:
                    data = str(getattr(item, name))
                    ws.write(row_num, col_num, data, font_style)
            except:
                ws.write(row_num, col_num," ", font_style)
            col_num += 1
    wb.save(response)
    return response
