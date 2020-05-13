function initiate_radar(id_selected, info_project){
   var data = [{
      type: 'scatterpolar'
   }];

   var layout = {
      polar : {
         radialaxis: {
            visible: false,
         },
         angularaxis : {
            showticklabels: false,
            dtick:360/5
         },
      },
      showlegend: false,
      title : "Choisissez un projet",
      font: {
         family : 'LMSans-regular'
      },
   };

   var config = {
      responsive: true,
      displayModeBar : false
   };


   Plotly.newPlot("div_plot", data, layout, config);
}



function plot_taskradar(id_selected, info_project, container = 'div_plot'){

   // Initialisation des donnees
   var selected_project = info_project[info_project.findIndex(proj => proj.id === id_selected)];

   var members = [];
   var num_tasks = [];
   var title = selected_project.name;

   selected_project.members.forEach((item, index) => {
      members.push(item.name);
      num_tasks.push(parseInt(item.count));
   })

   members.push(selected_project.members[0].name);
   num_tasks.push(selected_project.members[0].count);


   // Plot
   var data = [{
      type: 'scatterpolar',
      r: num_tasks,
      theta: members,
      name: "",
      fill: 'toself',
      hovertemplate : "Utilisateur : %{theta}<br>Nombre de tâches : %{r}"
   }];

   var layout = {
      polar : {
         radialaxis: {
            visible: true,
            dtick: 1
            }
         },
      showlegend: false,
      title : title,
      font: {
         family : 'LMSans-regular'
      },
   };

   var config = {
      responsive: true,
      displayModeBar : false
   };

   Plotly.newPlot(container, data, layout, config);
}



function plot_taskhistogram(id_selected, info_project, container = 'div_plot'){
   var selected_project = info_project[info_project.findIndex(proj => proj.id === id_selected)];

   var members = [];
   var num_tasks = [];
   var title = selected_project.name;

   selected_project.members.forEach((item, index) => {
      members.push(item.name);
      num_tasks.push(parseInt(item.count));
   })

   var data = [{
      type: 'bar',
      x : members,
      y : num_tasks,
      text: num_tasks.map(String),
      textposition: 'auto',
      hoverinfo: 'none',
      marker: {
         color: 'rgb(127,127,127)',
         opacity: 0.6,
         line: {
            color: 'rgb(80,80,80)',
            width: 1.5
         }
      }
   }];

   var layout = {
      showlegend: false,
      title : title,
      font: {
         family : 'LMSans-regular'
      },
      xaxis: {
         tickangle: -45
      },
      yaxis: {
         title: '# de tâches'
      },
      bargap :0.05
   };

   var config = {
      responsive: true,
      displayModeBar : false
   };

   Plotly.newPlot(container, data, layout, config);
}
