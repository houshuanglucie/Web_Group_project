// https://visjs.github.io/vis-timeline/examples/timeline/
// https://www.rgraph.net/canvas/docs/gantt.html

// ===== Initialisation et tracage du diagramme de Gantt pour le calendrier ======
var groups = new vis.DataSet();
var items = new vis.DataSet();

function initialize_gantt(tasks_by_project){
   var n = 0;

   for (var i = 0; i < tasks_by_project.length; i++) {
      project = tasks_by_project[i];

      groups.add({
         id: i,
         content: project.project,
         order: i,
      });

      // 1588576194
      // 1588576156060

      for(var j = 0 ; j < project.tasks.length ; j++){
         task = project.tasks[j];
         items.add({
            id: n,
            group: i,
            start: parseInt(task.start),
            end: parseInt(task.end),
            type: "range",
            content: task.name,
         });

         n++;
      }
   }
}



function plot_gantt(){

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

   // create a Timeline
   var container = document.getElementById("gantt");
   timeline = new vis.Timeline(container, null, options);
   timeline.setGroups(groups);
   timeline.setItems(items);


}
