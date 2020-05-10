var groups = new vis.DataSet();
var items = new vis.DataSet();

var where_plot = null;
var id_selected = 0;
var type_view = null;


// ===== Initialisation de tous les clicks possibles ======
function init_interactivity(){

   for(var i = 1 ; i < 5 ; i++){
      const name_board = 'board' + i.toString();
      const id_select = '#view_board' + i.toString(); // form to select

      // Quand on selectionne une vue
      $(id_select).on('change', function(){
         view_selected = $(id_select).find(":selected").val();
         type_view = view_selected;
         where_plot = name_board;

         if(view_selected == "tasks"){
            // On a rien a envoyer, on a déjà tout recu des le chargement de la page
            clone_task_view = document.getElementById('tasks_views').cloneNode(true);
            clone_task_view.id = 'tasks_views' + name_board;
            document.getElementById(name_board).appendChild(clone_task_view);
            $('#tasks_views' + name_board).show();
            $(id_select).hide();
         }

         else if(view_selected == "gantt"){
            send_ajax_dash(name_board);
            $(id_select).hide();
         }

         else if(view_selected == "burndown"){
            document.getElementById(name_board).appendChild(document.getElementById('select_project'));
            $('#select_project').show();
         }

         else if(view_selected == "radartask"){
            document.getElementById(name_board).appendChild(document.getElementById('select_project'));
            $('#select_project').show();

         }

         else if(view_selected == "radaractivity"){
            send_ajax_dash(name_board);
         }
      });
   }


   // Quand on a la selection de projet qui s'affiche et qu'on selectionne un projet
   $('#select_project').on('change', function() {
      id_selected = parseInt($('#select_project').find(":selected").val());
      send_ajax_dash(where_plot);
      $('#view_' + where_plot).hide();
      $('#select_project').hide();
   });
}


// ===== Récupération de données du serveur en asynchrone ======
function send_ajax_dash(board){
   var title = "";
   $.ajax({
      url : url_endpoint,
      type : "POST",
      data : {
         'csrfmiddlewaretoken' : $("[name = csrfmiddlewaretoken]").val(),
         'type_view' : type_view
      },

      success : function(json) { // Si on recoit une erreur 200
         // console.log("SUCCESS");
         // console.log(json);
         handle_response(type_view, json, board);


      },

      error : function(json, err) { // Si on recoit une erreur 400
         // console.log("FAILED");
         // console.log(err);
      }
   });
}


//  ===== Ce qu'on fait quand on recoit une reponse ======
function handle_response(type_view, json, board){

   if(type_view == "gantt"){
      var tasks_by_project = json.tasks;
      initialize_gantt(tasks_by_project);
      plot_gantt(board, false);
      removeoption(where_plot, "gantt");
   }

   else if(type_view == "burndown"){
      var info_project = json.info;
      plot_burndown(id_selected, info_project, where_plot);
      removeoption(where_plot, "burndown");
   }

   else if(type_view == "radartask"){
      var info_project = json.info;
      plot_taskhistogram(id_selected, info_project, where_plot);
      removeoption(where_plot, "radartask");
   }

   else if(type_view == "radaractivity"){
      var info_plot = json.traces;
      plot_radaractivity(info_plot, "Mes activités sur l'application", where_plot);
      removeoption(where_plot, "radaractivity");
   }

}
//  ===== On enleve la possibilité de choisir ce graphe dans un autre board ======
function removeoption(where, what){
   var number_board = parseInt(where[where.length - 1]);

   for(var i = 1 ; i < 5; i++){
      if(i !== number_board){
         $(`#view_box${i}_choice option[value='${what}']`).remove();
      }
   }

}
