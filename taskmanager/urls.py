from django.urls import path
from . import views
from . import views_graph
from . import views_export

urlpatterns = [
    path('', views.redirect_home, name='redirect_home'),
    path('home/', views.home, name='home'),
    # path('connect/', views.connect, name = 'connect'),
    path('connect/', views.LoginPage.as_view(), name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:id>', views.focus_project, name='focus_project'),
    path('task/<int:id>', views.focus_task, name='focus_task'),
    path('newproject', views.newproject, name='newproject'),
    path('manageproject/<int:id>', views.manageproject, name='manageproject'),
    path('newtask/<int:id_project>', views.newtask, name='newtask'),
    path('managetask/<int:id>', views.managetask, name='managetask'),

    path('members/', views.projects_members, name='membersproject'),
    path('tasks/', views.list_tasks, name='listtasks'),
    path('finished/', views.finished_tasks, name='finishedtasks'),
    path('distinct/<int:ide>', views.distinct_tasks, name='distincttasks'),
    path('activities/<int:ide>', views.activities, name='activities'),

    path('dashboard', views_graph.dashboard, name='dashboard'),
    path('graphs', views_graph.graphs, name='graphs'),

    path('gantt', views_graph.gantt, name='gantt'),

    path('burndown', views_graph.burndown, name='burndown'),
    path('radartask', views_graph.radartask, name='radartask'),
    path('radaractivity', views_graph.radaractivity, name='radaractivity'),
    path('manageapp', views_graph.manageapp, name='manageapp'),

    path('taskfilter/', views.task_filter, name='task_filter'),

    path('export/xml/<int:id>', views_export.export_xml, name='export_xml'),
    path('export/json/<int:id>', views_export.export_json, name='export_json'),
    path('export/csv/<int:id>', views_export.export_csv, name='export_csv'),
    path('export/excel/<int:id>', views_export.export_excel, name='export_excel'),
]
