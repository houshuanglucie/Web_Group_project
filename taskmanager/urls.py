from django.urls import path
from . import views

urlpatterns = [
	path('', views.redirect_home, name = 'redirect_home'),
	path('home/', views.home, name = 'home'),
	path('connect/', views.connect, name = 'connect'),
	path('disconnect/', views.disconnect, name = 'disconnect'),
	path('projects/', views.projects, name = 'projects'),
	path('projects/<int:id>', views.focus_project, name = 'focus_project'),
]
