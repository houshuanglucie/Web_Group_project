from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length = 160, verbose_name = "Titre")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "Membres")

    def __str__(self):
        return self.name


class Status(models.Model):
    how = models.CharField(max_length = 160, verbose_name = "Statut")
    def __str__(self):
        return self.how

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Utilisateur")
    submit_time = models.DateTimeField(default = timezone.now, verbose_name = "Date")
    content = models.TextField(null = True, verbose_name = "Contenu", blank = True)

    def __str__(self):
        return self.user + " : " + self.content


class Task(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE, verbose_name = "Projet")
    name = models.CharField(max_length = 200, verbose_name = "Tâche")
    description = models.TextField(null = True, verbose_name = "Description", blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Responsable")
    start_date = models.DateTimeField(verbose_name = "Date de début")
    due_date = models.DateTimeField(verbose_name = "Deadline")
    priority = models.IntegerField()
    status = models.ForeignKey('Status', on_delete = models.CASCADE, verbose_name = "Statut")
    comments = models.ManyToManyField(Comment, related_name = "Commentaires", blank = True)

    def __str__(self):
        return self.name
# TODO Checker que start_date < due_date
