from django.contrib import admin
from .models import Project, Task, Status, Comment

# Register your models here.
# Users :
# vt - vtawng20
# sibelius - concertoinDMinor
# tchaikovsky - concertoinDMajor
# paganini - caprice24
# bach - aironGString

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', )

class StatusAdmin(admin.ModelAdmin):
    list_display = ('how', )
    list_filter = ('how', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'submit_time', )
    list_filter = ('user', )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', )
    list_filter = ('project', 'status', )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task, TaskAdmin)
