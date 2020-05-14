# Gestionnaire de projets

*Projet collectif du module AWNG - Avril / Mai 2020*

## Contenu implémenté

### F1 - Visualisation de toutes les données saisies

### F2 - Filtrage et tri

### F3 - Export

### F4 - Graphes
- Diagramme de Gantt
- Burndown chart
- Radars des tâches et des activités (globales et par projet)
- Tableau de bord personnalisable (jusque dans une certaine mesure)
- *[Super-utilisateur]* Réseau d'activités entre utilisateurs et vue des utilisateurs les plus actifs
<br>

## Contenus qui pourraient être améliorés

### F4 - Graphes 
- Rendre le tableau de bord plus intéractif (choix de la taille des cadres, du nombre de cadres...)
- Tri par timestamp pour les radars de taches ou d'activités
- Présentation du diagramme de Gantt un peu austère...

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
`user<N>` : *`bar`* où N est un entier  

***
