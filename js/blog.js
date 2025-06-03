Promise.all([
    fetch('./assets/blog_posts/nodes.json').then(res => res.json()),
    fetch('./assets/blog_posts/links.json').then(res => res.json()),
    fetch('./assets/blog_posts/articles.json').then(res => res.json())
]).then(([nodes, links, articles]) => {
    renderGraph(nodes, links, articles);
});

function renderGraph(nodes, links, articles) {
    const width = document.querySelector('#graph').clientWidth;
    const height = document.querySelector('#graph').clientHeight;

    const svg = d3.select("#graph");
    svg.selectAll("*").remove();

    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(d => 100 / d.weight))
        .force("charge", d3.forceManyBody().strength(-150))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .velocityDecay(0.4);

    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => d.weight);

    const zoom = d3.zoom()
        .on("zoom", (event) => {
            svgGroup.attr("transform", event.transform);
        })
        .filter((event) => event.type !== "dblclick"); // Disable zoom on double click

    d3.select("svg").call(zoom);


    const node = svg.append("g")
        .selectAll("g")
        .data(nodes)
        .join("g")
        .attr("class", "node");

    node.append("circle")
        .attr("r", 10)
        .attr("fill", "#69b3a2")
        .on("mouseover", function (event, d) {
            d3.select(this).transition().attr("r", 20);
            highlight(d.id, true);
        })
        .on("mouseout", function (event, d) {
            d3.select(this).transition().attr("r", 10);
            highlight(d.id, false);
        })
        .on("click", function (event, d) {
            document.getElementById("article-title").innerText = d.title;
            document.getElementById("article-date").innerText = d.date;
            document.getElementById("article-content").innerText = articles[d.id];
        })
        .call(drag(simulation))
        .on("dblclick", (event, d) => {
            // Prevent default zoom or focus
            event.preventDefault();
            event.stopPropagation();
        });

    node.append("text")
        .text(d => d.title)
        .attr("x", 15)
        .attr("y", 5)
        .style("fill", "white");

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("transform", d => `translate(${d.x},${d.y})`);
    });


    function highlight(id, on) {
        link.attr("stroke", d =>
            d.source.id === id || d.target.id === id ? (on ? "yellow" : "#999") : "#999"
        );
    }

    function drag(simulation) {
        return d3.drag()
            .on("start", (event, d) => {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            })
            .on("drag", (event, d) => {
                d.fx = event.x;
                d.fy = event.y;
            })
            .on("end", (event, d) => {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            });
    }

    svg.call(d3.zoom().on("zoom", ({ transform }) => {
        svg.selectAll("g").attr("transform", transform);
    }));
}
