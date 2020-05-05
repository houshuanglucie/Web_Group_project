// https://visjs.github.io/vis-timeline/examples/timeline/
// https://www.rgraph.net/canvas/docs/gantt.html

// ===== Initialisation du diagramme de Gantt pour le calendrier ======
var groups = new vis.DataSet();
var items = new vis.DataSet();

function initialize_gantt(tasks_by_project){
   var n = 0;

   for (var i = 0; i < tasks_by_project.length; i++) {
      project = tasks_by_project[i];

      // Ajout d'un groupe de taches (ie un projet)
      groups.add({
         id: i,
         content: project.project,
         order: i,
      });

      for(var j = 0 ; j < project.tasks.length ; j++){
         task = project.tasks[j];
         // Ajout de taches dans un projet
         items.add({
            id: n,
            group: i,
            start: parseInt(task.start),
            end: parseInt(task.end),
            type: "range",
            content: task.name,
            name_project_parent : task.project_name,
            id_project_parent : task.project_id,
            id_task : task.id_task,
         });

         n++;
      }
   }
}


// ===== Tracage du diagramme de Gantt pour le calendrier ======
function plot_gantt(){

   // GRAPHICS
   var now = Date.now();

   var options = {
     stack: true,
     maxHeight: 640,
     horizontalScroll: false,
     verticalScroll: true,
     zoomKey: "ctrlKey",
     start: Date.now() - 1000 * 60 * 60 * 24 * 3, // minus 3 days
     end: Date.now() + 1000 * 60 * 60 * 24 * 31, // plus 1 months aprox.
     orientation: {
       axis: "both",
       item: "top",
     },
   };


   var container = document.getElementById("gantt");
   timeline = new vis.Timeline(container, null, options);
   timeline.setGroups(groups);
   timeline.setItems(items);

   // INTERACTIONS
   timeline.on("click", function (properties) {
      has_clicked(properties);
   });

   timeline.on("itemover", function (properties) {
      has_clicked(properties);
   });

   document.getElementById("waiting").style = "display:none";

   }


// ===== Mise a jour du div details quand on hover une tache ======
function has_clicked(properties) {
   var item_clicked = items.get(properties.item);
   var details_div = document.getElementById("details_task");
   console.log(item_clicked);
   if(item_clicked.content != undefined){
      details_div.style = "display:block";
      make_details(item_clicked);
   }
   else{
      details_div.style = "display:none";
   }
}



// ===== Definition du nouveau contenu ======
function make_details(item){

   const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour : 'numeric', minute : 'numeric'};
   var name = item.content;
   var project_name = item.name_project_parent;
   var project_id = item.id_project_parent;
   var start_date = new Date(item.start).toLocaleDateString('fr-FR', options);
   var due_date = new Date(item.end).toLocaleDateString('fr-FR', options);
   var id_task = item.id_task;

   document.getElementById("details_name").innerHTML = name;
   document.getElementById("details_project").href = "/projects/" + project_id;
   document.getElementById("details_project").innerText = project_name;
   document.getElementById("details_start").innerHTML = start_date;
   document.getElementById("details_deadline").innerHTML = due_date;
   document.getElementById("details_link").href = "/taskmanager/task/" + id_task;


}
