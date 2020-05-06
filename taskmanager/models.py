from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
import os


# ===== Projet =====
class Project(models.Model):
    # Nom du projet
    name = models.CharField(max_length = 160, verbose_name = "Titre")
    # Liste des membres
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "Membres")
    # Visibilité du projet (Prive ou public)
    public = models.CharField(max_length = 2, choices = [("PU", "public"), ("PR", "privé")], default = "PR", verbose_name = "Partage")

    def __str__(self):
        return self.name


# ===== Statut =====
# En gros une classe qui remplace un CharField avec choices
class Status(models.Model):
    # Statut [Nouvelle, En attente, ...]
    how = models.CharField(max_length = 160, verbose_name = "Statut")

    def __str__(self):
        return self.how


# ===== Commentaire =====
# Journal d'une tache Ou commentaires, selon comment on voit ca...
class Comment(models.Model):
    # L'user qui a ecrit le commentaire
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Utilisateur")
    # Quand le commentaire a ete ajoute
    submit_time = models.DateTimeField(default = timezone.now, verbose_name = "Date")
    # Son contenu
    content = models.TextField(null = True, verbose_name = "Contenu", blank = True)

    def __str__(self):
        return self.user.username + " : " + self.content


# ===== Sous tache d'une tache =====
class Subtask(models.Model):
    # Tache parent
    task = models.ForeignKey('Task', on_delete = models.CASCADE, verbose_name = "Parent", default = None )
    # Nom de la sous tache
    name = models.CharField(max_length = 100, verbose_name = "Sous-tâche")

    def __str__(self):
        return self.name


# ===== Categorie d'une tache =====
class Category(models.Model):
    # Nom de la categorie
    name = models.CharField(max_length = 100, verbose_name = "Catégorie")

    def __str__(self):
        return self.name



# ===== Tache =====
class Task(models.Model):
    # Projet parent
    project = models.ForeignKey('Project', on_delete = models.CASCADE, verbose_name = "Projet")
    # Nom de la tache
    name = models.CharField(max_length = 200, verbose_name = "Tâche")
    # Description de la tache
    description = models.TextField(null = True, verbose_name = "Description", blank = True)
    # Categorie de la tache
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, verbose_name = "Catégorie", null = True, blank = True)
    # Responsable de la tache [assignee]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, verbose_name = "Responsable")
    # Une piece jointe pour expliciter le propos
    attachment = models.FileField(upload_to = "file/", null = True, blank = True, verbose_name = "Pièce jointe")
    # Début de la tache
    start_date = models.DateTimeField(verbose_name = "Date de début")
    # Deadline de la tache
    due_date = models.DateTimeField(verbose_name = "Deadline")
    # Priorité de la tache
    priority = models.IntegerField(verbose_name = "Priorité")
    # Statut [Nouvelle, En attente...]
    status = models.ForeignKey('Status', on_delete = models.CASCADE, verbose_name = "Statut")
    # Journal (ou commentaires...)
    comments = models.ManyToManyField(Comment, related_name = "Commentaires", blank = True)


    # Permet d'avoir le nom et l'extension de la piece jointe
    def attachment_info(self):
        _, extension = os.path.splitext(self.attachment.name)
        name = os.path.basename(self.attachment.name)
        return name, extension


    def __str__(self):
        return self.name


class Project_members(models.Model):

    project = models.OneToOneField(Project,on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "Membres")
    number = models.IntegerField()
