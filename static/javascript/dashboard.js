var groups = new vis.DataSet();
var items = new vis.DataSet();

var where_plot = null;
var id_selected = 0;


function init_interactivity(){

   for(var i = 1 ; i < 5 ; i++){
      const name_board = 'board' + i.toString();
      const id_select = '#view_board' + i.toString();

      $(id_select).on('change', function(){
         view_selected = $(id_select).find(":selected").val();

         if(view_selected == "tasks"){
            document.getElementById(name_board).appendChild(document.getElementById('tasks_views'));
            $('#tasks_views').show();
            $(id_select).hide();
         }

         else if(view_selected == "gantt"){
            send_ajax("gantt", name_board);
            $(id_select).hide();
         }

         else if(view_selected == "burndown"){
            document.getElementById(name_board).appendChild(document.getElementById('select_project'));
            $('#select_project').show();
            where_plot = name_board;
         }

         else if(view_selected == "NULL"){
            console.log("NULL");
         }

      });
   }



   $('#select_project').on('change', function() {
      id_selected = parseInt($('#select_project').find(":selected").val());
      send_ajax("burndown", where_plot);
      $('#view_' + where_plot).hide();
      $('#select_project').hide();
   });
}


function send_ajax(type_view, board){
   var title = "";
   $.ajax({
      url : url_endpoint,
      type : "POST",
      data : {
         'csrfmiddlewaretoken' : $("[name = csrfmiddlewaretoken]").val(),
         'type_view' : type_view
      },

      success : function(json) { // Si on recoit une erreur 200
         console.log("SUCCESS");
         console.log(json);
         handle_response(type_view, json, board);


      },

      error : function(json, err) { // Si on recoit une erreur 400
         console.log("FAILED");
         console.log(err);
      }
   });
}



function handle_response(type_view, json, board){

   if(type_view == "gantt"){
      var tasks_by_project = json.tasks;
      initialize_gantt(tasks_by_project);
      plot_gantt(board, false);
   }

   else if(type_view == "burndown"){
      var info_project = json.info;
      plot_burndown(id_selected, info_project, where_plot);
   }

}
