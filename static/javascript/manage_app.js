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
      interaction: {
         hover: true
      },
      nodes: {
         shape: "dot",
      },
      edges: {
         smooth: {
            type : "continuous",
            forceDirection : "none",
            roundness : 1
         }
      },
      physics: {
         repulsion: {
            springConstant: 0,
            nodeDistance: 115
         },
         minVelocity: 0.75,
         solver: "repulsion"
      },

      configure: {
         enabled: false,
         filter: 'physics, layout',
         showButton: true
      }


      };

   var network = new vis.Network(container, data, options);

}
