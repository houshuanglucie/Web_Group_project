function init_graph(){

   var layout = {
      showlegend: false,
      title : "Choisissez un projet",
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

function linspace(startValue, stopValue, card){
   var arr = [];
   var step = (stopValue - startValue) / (card - 1);
   for(var i = 0 ; i < card ; i++){
      arr.push(Math.round(startValue + (step*i)));
   }
   return arr;
}



function plot_graph(id_selected, info_project){

   var selected_project = info_project[info_project.findIndex(proj => proj.id_project === id_selected)];
   var title = selected_project.name_project;
   var tasks_data = selected_project.tasks_data;

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

      Plotly.newPlot('div_plot', data, layout, config);
      return;
   }

   var data = [];

   var n_tasks = tasks_data.length;
   var min_date = tasks_data[0].start_date;
   var max_date = tasks_data[n_tasks - 1].due_date;


   tasks_data.forEach((task, index) => {
      var x_list = [];
      var y_list = [];
      var interpol = linspace(task.start_date, task.due_date, 20);
      var a = 100/(task.due_date - task.start_date)

      interpol.forEach((x, index) => {
         y_list.push(a * (x - task.start_date));
         x_list.push(new Date(x));
      })

      var trace = {
         x: x_list,
         y: y_list,
         name: task.shorten_name,
         mode: 'lines',
         type: 'scatter',
         line: {
            dash: 'dot',
            width: 1
         },
         hovertemplate : "Tâche : " + task.name + "<br>Date : %{x|%d/%m/%Y}<br>Réalisé théoriquement : %{y:.0f} %"
      };

      data.push(trace);


      if(task.start_date < min_date) {min_date = task.start_date;}
      if(task.due_date > max_date) {max_date = task.due_date;}
   });

   var x_project = [];
   var y_project = [];


   var interpol = linspace(min_date, max_date, 100);

   interpol.forEach((timestamp, index) =>{
      var sum_prct = 0;

      tasks_data.forEach((task, index) => {
         var a = 100/(task.due_date - task.start_date);
         if(task.start_date > timestamp){
            sum_prct += 0;
         }
         else if(task.due_date < timestamp){
            sum_prct += 100
         }
         else{
            sum_prct += (a * (timestamp - task.start_date));
         }
      });

      x_project.push(new Date(timestamp));
      y_project.push(sum_prct/(n_tasks));
   });


   var trace_project = {
      x: x_project,
      y: y_project,
      name: title,
      mode: 'lines',
      type: 'scatter',
      line: {
         width: 3
      },
      hovertemplate : "<b>Projet global</b><br>Date : %{x|%d/%m/%Y}<br>Réalisé théoriquement : %{y:.0f} %"
   };

   data.push(trace_project);





   var layout = {
      showlegend: true,
      title : title + "<br>",
      hovermode : 'closest',
      xaxis : {
         tickformat : "%d/%m<br>%Y"
      },
      yaxis : {
         title : "% réalisés"
      }
   };


   var config = {
      responsive: true,
      displayModeBar : false
   };

   Plotly.newPlot('div_plot', data, layout, config);
}
