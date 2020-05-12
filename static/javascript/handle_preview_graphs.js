function handle_preview_graphs(){

   $('#dropdown_menu').hover(function(){
      $('.description').fadeIn(300);
   },
   function(){
      $('.description').fadeOut(200);
   })

   // CUSTOM DASHBOARD
   $('#dashboard-nav_item').hover(function() {
      $('#name_graph').text("Tableau de bord");
      $('#description_graph').text("Un tableau de bord customisable avec les représentations que vous choisissez");
      $('#image_graph').attr("src", "../../static/pictures/graphs_preview/dashboard.png");
   });

   // GANTT
   $('#gantt-nav_item').hover(function() {
      $('#name_graph').text("Diagramme de Gantt");
      $('#description_graph').text("Une vue temporelle de vos projets et de vos activités");
      $('#image_graph').attr("src", "../../static/pictures/graphs_preview/gantt.png");
   });

   // BURNDOWN
   $('#burndown-nav_item').hover(function() {
      $('#name_graph').text("Burndown chart");
      $('#description_graph').text("Une représentation de votre avancée dans chaque tâche et projet");
      $('#image_graph').attr("src", "../../static/pictures/graphs_preview/burndown.png");
   });


   // RADAR TASK
   $('#radartask-nav_item').hover(function() {
      $('#name_graph').text("Radar des tâches");
      $('#description_graph').text("Pour voir qui va beaucoup travailler dans vos projets");
      $('#image_graph').attr("src", "../../static/pictures/graphs_preview/tasks.png");
   });


   // RADAR ACTIVTY
   $('#radaractivity-nav_item').hover(function() {
      $('#name_graph').text("Radar d'activités");
      $('#description_graph').text("Pour voir si VOUS travaillez beaucoup dans vos projets");
      $('#image_graph').attr("src", "../../static/pictures/graphs_preview/activity.png");
   });
}
