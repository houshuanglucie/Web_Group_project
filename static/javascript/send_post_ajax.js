/**
*  Fonction qui gere le POST a la place de Django automatiquement
*  A cause du drag and drop qui n'est pas vraiment un champ que Django comprend
*  J'ignore s'il existe une methode plus simple
**/
function post_form(url_endpoint, action){
   /*
      args :
         url_endpoint : où on va après avoir envoyé la requête
         action : ce que l'user a fait CHOICES = [add, save, delete]
   */
   // Liste qu'on va envoyer
   var members_chosen = [];

   // Tous les enfants du div contenant les membres du projet, ie les boites avec les noms des membres du projet
   const members = $(".place_member").children();

   // Pour toutes les boites membres, on prend son nom et on le met dans la liste a envoyer
   for(var i = 0 ; i < members.length ; i++){
      var member = members[i];
      if(member.className.includes("member_box")){
         members_chosen.push(member.firstChild.data);
      }
   }

   // Si le projet est public ou pas
   var check_val = $("input[name='publicCheck']:checked").val()

   // console.log($("[name = csrfmiddlewaretoken]").val());
   // console.log(members_chosen);
   // console.log($("[name = name]").val())
   // console.log(action);

   // Envoi de la requête au serveur.
   // Juste une requête normale comme si on avait utilisé que Django, mais on l'a fait a la main
   $.ajax({
      url : url_endpoint,
      type : "POST",
      data : {
         'csrfmiddlewaretoken' : $("[name = csrfmiddlewaretoken]").val(),
         'name' : $("[name = name]").val(),
         'members' : members_chosen,
         'publicCheck' : check_val,
         'action' : action,
      },

      success : function(json) { // Si on recoit une erreur 200
         // console.log("SUCCESS");
         // console.log(json);
         
         if(action == 'save'){
            // On affiche le toast "Modification"
            $("#toast_body")[0].firstChild.data = json.name + " a été modifié.";
            $('#toast_valid').css("z-index", "10");
            $('#toast_valid').toast('show');
         }
         else if(action == 'delete'){
            // On redirige vers la page des projets
            // Et on fuit l'erreur aussi, vu que la page n'existe a priori plus (python a supprimé le projet)
            window.location.href = "/taskmanager/projects";
         }
         else {
            // On affiche le toast "Ajout"
            $("#toast_body")[0].firstChild.data = json.name + " a été crée.";
            $('#toast_valid').toast('show');
         }
      },

      error : function(json, err) { // Si on recoit une erreur 400
         // console.log("FAILED");
         // console.log(err);
         $('#toast_member').toast('show');
      }
   });
}
