# Gestionnaire de projets

*Projet personnel du module AWNG - Avril / Mai 2020*

## Contenu implémenté

<br>

## Contenus qui pourraient être améliorés


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
`tchaikovsky` : *`concertoinDMajor`* *(utilisateur qui a le plus de données intéressantes dans la base)*  
`sibelius` : *`concertoinDMinor`*  
`paganini` : *`caprice24`*  
`bach` : *`aironGString`*  
`massenet` : *`thaisMeditation`*  
`vt` : *`vtawng20`* *(superuser, mais sans beaucoup de données me concernant)*  

***
