# Gestionnaire de projets

*Projet personnel du module AWNG - Avril / Mai 2020*

## Contenu implémenté
- __[Objectif]__ Classes projets / tâches associées à leur pages de création, modification et visualisation globale ou individuelle
- Ajout d'attributs dans les différents classes *(projet public/privé ; pièce jointe, catégories et sous-tâches pour les tâches)*
- Graphismes :
   - Responsivité (du moins majoritairement... cf. plus bas)
   - D'autres fioritures (messages, drag & drop, ...)
- D'autres fonctionnalités plus ou moins utiles *(tableau de  bord, calendrier)*

<br>

## Contenus qui pourraient être améliorés
- Prise en compte des fuseaux horaires : je me suis résolu à mettre `USE_TZ = False` qui me causait des problèmes...
- Ordre d'affichage des tâches pas vraiment réfléchie :
   - Actuellement en fonction seulement de la priorité, mais le statut devrait peut-être être pris en compte. Voire il faudrait changer toute la vue.
- Robustesse du programme :
   - Un utilisateur peut créer un projet privé pour quelqu'un d'autre. Pourquoi pas, mais pas très logique...
   - Un non-membre d'un projet privé peut encore avoir accès à un projet privé ne le concernant pas à partir de son URL : je n'ai pas géré ce cas là...
- Responsivité : l'application est responsive, sauf sur les écrans verticaux très étroits


## En pratique...
#### *Pour se rendre sur la bonne page*
*À exécuter sur un terminal / invite de commandes avec* `python` *ou* `python3`
1. Lancer une migration `python manage.py migrate`  
2. Charger la base de données `python manage.py loaddata db.json`  
3. Lancer le serveur `python manage.py runserver`
4. Se rendre sur `localhost:8000` : ça vous redirigera vers la bonne page.  



<br>

#### *Utilisateurs enregistrés dans la base db.json*
`tchaikovsky` : *`concertoinDMajor`* *(utilisateur qui a le plus de données intéressantes dans la base)*  
`sibelius` : *`concertoinDMinor`*  
`paganini` : *`caprice24`*  
`bach` : *`aironGString`*  
`massenet` : *`thaisMeditation`*  
`vt` : *`vtawng20`* *(superuser, mais sans beaucoup de données me concernant)*  

***
