from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
import os


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

class Subtask(models.Model):
    task = models.ForeignKey('Task', on_delete = models.CASCADE, verbose_name = "Parent", default = None )
    name = models.CharField(max_length = 100, verbose_name = "Sous-tâche")
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 100, verbose_name = "Catégorie")
    def __str__(self):
        return self.name


# Pour gerer que start_date < due_date, je fais confiance a javascript...
class Task(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE, verbose_name = "Projet")
    name = models.CharField(max_length = 200, verbose_name = "Tâche")
    description = models.TextField(null = True, verbose_name = "Description", blank = True)
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, verbose_name = "Catégorie", null = True, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Responsable")
    attachment = models.FileField(upload_to = "file/", null = True, blank = True, verbose_name = "Pièce jointe")
    start_date = models.DateTimeField(verbose_name = "Date de début")
    due_date = models.DateTimeField(verbose_name = "Deadline")
    priority = models.IntegerField(verbose_name = "Priorité")
    status = models.ForeignKey('Status', on_delete = models.CASCADE, verbose_name = "Statut")
    comments = models.ManyToManyField(Comment, related_name = "Commentaires", blank = True)

    def attachment_info(self):
        _, extension = os.path.splitext(self.attachment.name)
        name = os.path.basename(self.attachment.name)
        return name, extension


    def __str__(self):
        return self.name
