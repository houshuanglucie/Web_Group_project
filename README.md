# Gestionnaire de projets

*Projet collectif du module AWNG - Avril / Mai 2020*

## Contenu implémenté

### F1 - Visualisation de toutes les données saisies
- Implémentation de l'avancement des tâches et donc de celui du projet  
- Liste de projets et de membres  
- Liste des tâches avec attributs  
- Liste des tâches finies  
- Affichage des tâches de l'utilisateur et des autres membres d'un projet
- Page activités, tri par ordre chronologique

### F2 - Filtrage et tri
- Filtre par assigné, statut, date, et toute combinaison  
- Tri par assigné, statut, date  

### F3 - Export
- Export sous XML, JSON, CSV et Excel  
- Possiblité de sélection de la classe à exporter  
- Restriction de l'option aux superutilisateurs  

### F4 - Graphes
- Diagramme de Gantt et brundown chart
- Radars des tâches et des activités (globales et par projet)
- Tableau de bord "personnalisable"
- *[Super-utilisateur]* Réseau de projets entre utilisateurs et vue des utilisateurs les plus actifs

<br>

## En pratique...
#### *Pour se rendre sur la bonne page*
*À exécuter sur un terminal / invite de commandes avec* `python` *ou* `python3`
1. Lancer une migration `python manage.py migrate`  
2. Charger la base de données `python manage.py loaddata db.json`  
3. Lancer le serveur `python manage.py runserver`
4. Se rendre sur `localhost:8000` : ça vous redirigera vers la bonne page.  

<br>

#### *Pour créer plein de données*
1. Fermer le serveur (pour que ce soit un peu plus rapide...)  
2. Modifier la variable i dans create_data.py, selon ce qu'on veut faire (documentation dans le script)  
3. Lancer à partir de la racine `python manage.py shell < create_data.py`  

<br>

#### *Utilisateurs enregistrés dans la base db.json*
`vt` : *`vtawng20`* *(superuser)*  
`user<N>` : *`bar`* où N est un entier pas trop grand  
