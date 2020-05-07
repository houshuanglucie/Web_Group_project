from django.urls import path
from . import views
from . import views_graph

urlpatterns = [
	path('', views.redirect_home, name = 'redirect_home'),
	path('home/', views.home, name = 'home'),
	# path('connect/', views.connect, name = 'connect'),
	path('connect/', views.LoginPage.as_view(), name = 'connect'),
	path('disconnect/', views.disconnect, name = 'disconnect'),
	path('projects/', views.projects, name = 'projects'),
	path('projects/<int:id>', views.focus_project, name = 'focus_project'),
	path('task/<int:id>', views.focus_task, name = 'focus_task'),
	path('newproject', views.newproject, name = 'newproject'),
	path('manageproject/<int:id>', views.manageproject, name = 'manageproject'),
	path('newtask/<int:id_project>', views.newtask, name='newtask'),
	path('managetask/<int:id>', views.managetask, name='managetask'),
	path('dashboard', views.dashboard, name='dashboard'),

	path('calendar', views.calendar, name='calendar'),
	path('members/',views.projects_members, name='membersproject'),
	path('tasks/',views.list_tasks,name='listtasks'),
	path('finished/',views.finished_tasks,name='finishedtasks'),
	path('distinct/<int:ide>', views.distinct_tasks, name='distincttasks'),
	path('activities/<int:ide>', views.activities, name='activities'),

  path('graphs', views_graph.graphs, name='graphs'),
	path('gantt', views_graph.gantt, name='gantt'),
	path('activitydiag', views_graph.activitydiag, name='activitydiag'),
	path('burndown', views_graph.burndown, name='burndown'),
	path('radartask', views_graph.radartask, name='radartask'),
	path('radaractivity', views_graph.radaractivity, name='radaractivity'),


	path('projects/<int:id>/taskfilter', views.task_filter, name='task_filter'),
]
