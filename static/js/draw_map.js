function draw(url) {
    $.getJSON(url,function(data) {
        var network = null;
        // 下面是各种布局方案
        var directionInput = "UD"; // Up-Down
        // var directionInput = "DU"; // Down-Up
        // var directionInput = "LR"; // Left-Right
        // var directionInput = "RL"; // Right-Left
        var container = document.getElementById('mynetwork');
        var data = {
            nodes: data.nodes,
            edges: data.edges
        };
        var options = {
                physics:false
        };
        network = new vis.Network(container, data, options);
    });
}
