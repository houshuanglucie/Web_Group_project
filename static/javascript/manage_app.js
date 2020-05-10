function plot_network(nodes_server, edges_server){


   var nodes = new vis.DataSet(nodes_server);
   var edges = new vis.DataSet(edges_server);

   // create a network
   var container = document.getElementById("mynetwork");
   var data = {
     nodes: nodes,
     edges: edges
   };

   var options = {
      interaction: { hover: true },
      nodes: {
         shape: "dot",
         scaling: {
            customScalingFunction: function(min, max, total, value) {return value / total;},
            min: 5,
            max: 150
         }

      },
      edges: {
         smooth: {
            type : "continuous",
            forceDirection : "none",
            roundness : 1
         }
      },
      physics:{
         barnesHut : {
            gravitationalConstant : -28500,
         },
         minVelocity : 0.75

      }


      };

   var network = new vis.Network(container, data, options);

}
