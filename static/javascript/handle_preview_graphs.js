// TODO Faire gaffe a ce que si c'est deja affiche, on fade out pas
function handle_preview_graphs(){
   // GANTT
   $('#gantt-nav_item').hover(function() {
      $('#name_graph').text("Diagramme de Gantt");
      $('.description').fadeIn(300);
   },
   function() {
      $('.description').fadeOut(200);
   });


   // DIAGRAMME D'ACTIVITES
   $('#activitydiag-nav_item').hover(function() {
      $('#name_graph').text("Diagramme d'activités");
      $('.description').fadeIn(300);
   },
   function() {
      $('.description').fadeOut(200);
   });


   // BURNDOWN
   $('#burndown-nav_item').hover(function() {
      $('#name_graph').text("Burndown chart");
      $('.description').fadeIn(300);
   },
   function() {
      $('.description').fadeOut(200);
   });


   // RADAR TASK
   $('#radartask-nav_item').hover(function() {
      $('#name_graph').text("Radar des tâches");
      $('.description').fadeIn(300);
   },
   function() {
      $('.description').fadeOut(200);
   });


   // RADAR ACTIVTY
   $('#radaractivity-nav_item').hover(function() {
      $('#name_graph').text("Radar d'activités");
      $('.description').fadeIn(300);
   },
   function() {
      $('.description').fadeOut(200);
   });
}
