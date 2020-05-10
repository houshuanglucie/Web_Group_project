function initiate_radar(id_selected, info_project){
   var data = [{
      type: 'scatterpolar'
   }];
   Plotly.newPlot("div_plot", data);
}


function send_ajax(url_endpoint, range, project_id){
   var title = "";
   $.ajax({
      url : url_endpoint,
      type : "POST",
      data : {
         'csrfmiddlewaretoken' : $("[name = csrfmiddlewaretoken]").val(),
         'range' : range,
         'project_id' : project_id
      },

      success : function(json) { // Si on recoit une erreur 200
         // console.log("SUCCESS");
         // console.log(json);
         plot_radaractivity(json.traces, json.title);
      },

      error : function(json, err) { // Si on recoit une erreur 400
         // console.log("FAILED");
         // console.log(err);
      }
   });
}



function plot_radaractivity(info_plot, title, container = 'div_plot'){

   // Initialisation des donnees
   var axis = [];
   var count = [];

   info_plot.forEach((item, index) => {
      axis.push(item.axis);
      count.push(parseInt(item.count));
   })

   axis.push(info_plot[0].axis);
   count.push(info_plot[0].count);


   // Plot
   var data = [{
      type: 'scatterpolar',
      r: count,
      theta: axis,
      name :"",
      fill: 'toself',
      hovertemplate : "%{theta}<br># de traces : %{r}"
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
