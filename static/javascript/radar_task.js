function initiate_radar(id_selected, info_project){

   var data = [{
      type: 'scatterpolar'
   }];


   Plotly.newPlot("div_plot", data);

}

function plot_radar(id_selected, info_project){

   var selected_project = info_project[info_project.findIndex(proj => proj.id === id_selected)];

   var members = [];
   var num_tasks = [];

   selected_project.members.forEach((item, index) => {
      members.push(item.name);
      num_tasks.push(parseInt(item.count));
   })

   members.push(selected_project.members[0].name);
   num_tasks.push(selected_project.members[0].count);


   var data = [{
      type: 'scatterpolar',
      r: num_tasks,
      theta: members,
      name: selected_project.name,
      fill: 'toself',
      hovertemplate : "Utilisateur : %{theta}<br>Nombre de tâches : %{r}"
   }];

   var layout = {
      polar : {
      radialaxis: {
         visible: true,
         range: [0, 7]
         }
      },
      showlegend: false,
      title : selected_project.name
   };

   var config = {responsive: true};

   Plotly.newPlot("div_plot", data, layout, config);

   // new Chart(document.getElementById("div_plot"), {
   //    type: 'radar',
   //    data: {
   //       labels: members,
   //       datasets: [{
   //          label: selected_project.name,
   //          fill: true,
   //          backgroundColor: "rgba(120,120,120,0.2)",
   //          borderColor: "rgba(120,120,120,1)",
   //          pointBorderColor: "#fff",
   //          pointBackgroundColor: "rgba(120,120,120,1)",
   //          data: num_tasks
   //       }]
   //    },
   //    options: {
   //       title: {
   //          display: true,
   //          text: selected_project.name
   //       },
   //       tooltips: {
   //          enabled: true,
   //          callbacks: {
   //             label: function(tooltipItem, data) {
   //                return data.datasets[tooltipItem.datasetIndex].label + ' : ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
   //             }
   //          }
   //       },
   //       scale: {
   //          angleLines: {
   //             display: false
   //          },
   //          ticks: {
   //             suggestedMin: 0,
   //             suggestedMax: 10
   //          }
   //       }
   //    }
   //    });
}
