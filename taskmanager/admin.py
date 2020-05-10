from django.contrib import admin
from .models import Project, Task, Status, Comment, Subtask, Category
from .models import Verb, Trace

# Register your models here.
# Users :
# vt - vtawng20
# sibelius - concertoinDMinor
# tchaikovsky - concertoinDMajor
# paganini - caprice24
# bach - aironGString
# massenet - thaisMeditation

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'public')
    list_filter = ('public',)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('how', )
    list_filter = ('how', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'submit_time', )
    list_filter = ('user', )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', )
    list_filter = ('project', 'status', )

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'name', )
    list_filter = ('task', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )

class VerbAdmin(admin.ModelAdmin):
    list_display = ('verb', 'alias')
    list_filter = ('verb', )

class TraceAdmin(admin.ModelAdmin):
    list_display = ('actor', 'verb' )
    list_filter = ('actor','verb', )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Subtask, SubtaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Verb, VerbAdmin)
admin.site.register(Trace, TraceAdmin)
