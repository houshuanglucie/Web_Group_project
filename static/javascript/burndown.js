// ===== Tracage d'un graphe vide ======
function init_graph(){

   var layout = {
      showlegend: false,
      title : "Choisissez un projet",
      font: {
         family : 'LMSans-regular'
      },
      xaxis : {
         range : [0, 1],
         showticklabels: false
      },
      yaxis : {
         range : [0, 1],
         showticklabels: false
      }
   };

   var config = {
      responsive: true,
      displayModeBar : false
   };

   Plotly.newPlot('div_plot', [], layout, config);
}


// ===== Linspace de numpy ======
function linspace(startValue, stopValue, card){
   var arr = [];
   var step = (stopValue - startValue) / (card - 1);
   for(var i = 0 ; i < card ; i++){
      arr.push(Math.round(startValue + (step*i)));
   }
   return arr;
}

function print_date(timestamp){
   console.log(new Date(timestamp));
}


// ===== Tracage du burndown chart ======
function plot_burndown(id_selected, info_project, container = 'div_plot'){

   var selected_project = info_project[info_project.findIndex(proj => proj.id_project === id_selected)];
   var title = selected_project.name_project;
   var tasks_data = selected_project.tasks_data;




   // S'il n'y a aucune tâche
   if(tasks_data.length == 0){
      var layout = {
         showlegend: false,
         title : title + "<br><em>Aucune tâche</em>",
         xaxis : {
            range : [0, 1],
            showticklabels: false,
         },
         yaxis : {
            range : [0, 1],
            showticklabels: false,
         }
      };

      var config = {
         responsive: true,
         displayModeBar : false
      };

      Plotly.newPlot(container, data, layout, config);
      return;
   }



   var data = [];

   var n_tasks = tasks_data.length;
   var min_date = tasks_data[0].start_date;
   var max_date = tasks_data[n_tasks - 1].due_date;

   // ********************* PLOT DES TACHES THERIQUES & PRATIQUES ********************************
   // Pour chaque tache, on crée un plot qui est juste une fonction affine entre 0 et 100%
   // allant de start_date a due_date pour l'avancement théorique

   var timestamp_list_practical = [];
   var progress_list_practical = [];

   var d3colors = Plotly.d3.scale.category10();
   var color = 0;

   tasks_data.forEach((task, index) => {
      // ___________ Avancement théorique ______________
      var x_list = [];
      var y_list = [];
      var interpol = linspace(task.start_date, task.due_date, 20);
      var a = 100/(task.due_date - task.start_date);

      interpol.forEach((x, index) => {
         y_list.push(a * (x - task.start_date));
         x_list.push(new Date(x));
      });


      var trace = {
         x: x_list,
         y: y_list,
         legendgroup: task.shorten_name,
         name: task.shorten_name + " - théorique",
         mode: 'lines',
         type: 'scatter',
         line: {
            color: d3colors(color),
            dash: 'dot',
            width: 1
         },
         hovertemplate : "Tâche : " + task.name + "<br>Date : %{x|%d/%m/%Y}<br>Réalisé théoriquement : %{y:.0f} %"
      };

      data.push(trace);

      // ___________ Avancement pratique ______________
      var progress_traces = task.progress_traces;
      var x_list_practical = [];
      var y_list_practical = [];

      if(progress_traces.length == 0 && task.start_date < Date.now()){
         x_list_practical = [task.start_date, Date.now()];
         y_list_practical = [0, 0];
      }

      else if(progress_traces.length > 0){
         // Recherche de la date minimale
         min_date_practical = progress_traces[0].timestamp; // C'est vraiment le minimum car la liste est triée

         // Mise a jour de la date min pour l'avancement global du projet
         if(min_date_practical < min_date){
            min_date = min_date_practical;
         }

         // Si on a commencé la tache APRES la date théorique
         if(min_date_practical > task.start_date){
            x_list_practical.push(task.start_date);
            y_list_practical.push(0);
         }

         progress_traces.forEach((item, index) => {
            x_list_practical.push(item.timestamp);
            y_list_practical.push(item.progress);
         });

         // Pour faire un plateau jusqu'à aujourd'hui
         x_list_practical.push(Date.now());
         y_list_practical.push(progress_traces[progress_traces.length - 1].progress);

      }

      var trace_pratical = {
         x: x_list_practical,
         y: y_list_practical,
         legendgroup: task.shorten_name,
         name: task.shorten_name + " - pratique",
         mode: 'lines',
         type: 'scatter',
         line: {
            dash: 'longdashdot',
            width: 1,
            color: trace.line.color
         },
         hovertemplate : "Tâche : " + task.name + "<br>Date : %{x|%d/%m/%Y}<br>Réalisé en pratique : %{y:.0f} %"
      };

      timestamp_list_practical.push(x_list_practical);
      progress_list_practical.push(y_list_practical);


      data.push(trace_pratical);

      color++;

      // Recherche des dates extrêmes pour le plot du projet
      if(task.start_date < min_date) {min_date = task.start_date;}
      if(task.due_date > max_date) {max_date = task.due_date;}
   });




   // ********************* PLOT DE L'AVANCEMENT PROJET ********************************
   // Qui est la somme des autres burndowns/nb_taches

   var x_project = [];
   var y_project = [];
   var interpol = linspace(min_date, max_date, 100);
   interpol.push(Date.now());
   interpol.sort();

   var x_project_practical = [];
   var y_project_practical = [];

   interpol.forEach((timestamp, index) =>{
      var sum_prct = 0;
      var sum_prct_practical = 0;

      tasks_data.forEach((task, index) => {
         // ___________ Avancement théorique ______________
         var a = 100/(task.due_date - task.start_date);
         if(task.start_date > timestamp){ // Si au timestamp, la tache n'est pas commencée theoriquement
            sum_prct += 0;
         }
         else if(task.due_date < timestamp){ // Si au timestamp, la tache est finie theoriquement
            sum_prct += 100
         }
         else{ // Sinon, on interpole
            sum_prct += (a * (timestamp - task.start_date));
         }

         // ___________ Avancement pratique ______________
         var progress_traces = task.progress_traces;
         // Si y a aucune trace, l'avancee pratique vaut 0
         if(progress_traces.length == 0){
            sum_prct_practical += 0;
         }

         else{
            for(var i = 0 ; i < timestamp_list_practical[index].length-1 ; i++){
               var prec_time = timestamp_list_practical[index][i];
               var next_time = timestamp_list_practical[index][i+1];

               if(prec_time <= timestamp && timestamp <= next_time){
                  var prec_progress = progress_list_practical[index][i];
                  var next_progress = progress_list_practical[index][i+1];
                  var a = (next_progress - prec_progress)/(next_time - prec_time);
                  sum_prct_practical += (a * (timestamp - prec_time) + prec_progress);
               }
            }
         }



      });

      x_project.push(new Date(timestamp));
      y_project.push(sum_prct/n_tasks);

      if(timestamp < Date.now()){ // Si on est encore dans le passé, on peut ajouter l'avancement.
         x_project_practical.push(new Date(timestamp));
         y_project_practical.push(sum_prct_practical/n_tasks);
      }



   });


   var trace_project = {
      x: x_project,
      y: y_project,
      name: title + " - théorique",
      legendgroup: title,
      mode: 'lines',
      type: 'scatter',
      line: {
         width: 3,
         color: d3colors(color)
      },
      hovertemplate : "<b>Projet global</b><br>Date : %{x|%d/%m/%Y}<br>Réalisé théoriquement : %{y:.0f} %"
   };

   data.push(trace_project);

   var trace_project_practical = {
      x: x_project_practical,
      y: y_project_practical,
      name: title + " - pratique",
      legendgroup: title,
      mode: 'lines',
      type: 'scatter',
      line: {
         dash : 'longdashdot',
         width: 3,
         color : trace_project.line.color
      },
      hovertemplate : "<b>Projet global</b><br>Date : %{x|%d/%m/%Y}<br>Réalisé en pratique : %{y:.0f} %"
   };

   data.push(trace_project_practical);



   // ********************* PLOT DE LA LIGNE D'AUJOURD'HUI ********************************
   if(min_date <= Date.now() && Date.now() <= max_date ){
      now = new Date(Date.now());
      var trace_now = {
         x: [now, now],
         y: [0, 100],
         mode: 'lines',
         type: 'scatter',
         line: {
            width: 2,
            dash: 'dashdot',
            color: 'black'
         },
         name: "Aujourd'hui",
         hoverinfo : 'none',
         showlegend: false
      };

      data.push(trace_now);
   }



   // ********************* CONFIGURATION ********************************
   var margin_x_axis = 0.03 * (max_date - min_date); // 3% de la difference des dates

   var layout = {
      showlegend: true,
      legend:{
         font: {
            family: 'LMSans-regular'
         }
      },
      title : title + "<br>",
      hovermode : 'closest',
      xaxis : {
         range: [min_date-margin_x_axis, max_date+margin_x_axis],
         tickformat : "%d/%m<br>%Y"
      },
      yaxis : {
         title : {
            text : "% réalisés",
            font: {
               family : 'LMSans-regular'
            }
         },
      }
   };


   var config = {
      responsive: true,
      displayModeBar : false
   };


   Plotly.newPlot(container, data, layout, config);
}
