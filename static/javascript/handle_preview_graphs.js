function handle_preview_graphs(){

   $('#dropdown_menu').hover(function(){
      $('.description').fadeIn(300);
   },
   function(){
      $('.description').fadeOut(200);
   })

   // GANTT
   $('#gantt-nav_item').hover(function() {
      $('#name_graph').text("Diagramme de Gantt");
   });


   // DIAGRAMME D'ACTIVITES
   $('#activitydiag-nav_item').hover(function() {
      $('#name_graph').text("Diagramme d'activités");
   });


   // BURNDOWN
   $('#burndown-nav_item').hover(function() {
      $('#name_graph').text("Burndown chart");
   });


   // RADAR TASK
   $('#radartask-nav_item').hover(function() {
      $('#name_graph').text("Radar des tâches");
   });


   // RADAR ACTIVTY
   $('#radaractivity-nav_item').hover(function() {
      $('#name_graph').text("Radar d'activités");
   });
}
