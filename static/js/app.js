$(document).ready(function () {
  $("table").DataTable({
    pagingType: "simple",
  });
  var data = JSON.parse(document.getElementById("traces").getAttribute("data"));



  var width = 600;
  var height = 300;
  var padding = 30;
  var margin = 135;
  var adj = 20;
  // we are appending SVG first
  var svg = d3.select("#viz").append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "-" + adj + " -" + adj + " " + (width + adj) + " " + (height + adj))
    .style("margin", margin)
    .classed("svg-content", true);

  //-----------------------DATA PREPARATION------------------------//
  var dataset = data;
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(dataset, (d) => { return d.y })])
    .range([0, height - padding])


  svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", (d, i) => { return i * width / dataset.length + padding })
    .attr("y", (d) => { return height - yScale(d.y) })
    .attr("height", (d) => { return yScale(d.y) })
    .attr("width", width / dataset.length - (padding + margin))
    .attr("class", "bar")
    .append("title")
    .text((d) => { return d.y })


  svg.selectAll("text")
    .data(dataset)
    .enter()
    .append("text")
    .text((d) => { return d.y })
    .attr("x", (d, i) => { return i * width / dataset.length + (width / dataset.length - (padding + margin)) / 2 + 10 })
    .attr("y", (d) => { return height - yScale(d.y) - 25 })
    .style("font-size", "14px")
    .append("text")
    .text((d) => { return d.x })
    .attr("x", (d, i) => { return i * width / dataset.length + (width / dataset.length - (padding + margin)) / 2 + 10 })
    .attr("y", (d) => { return yScale(d.y) - 15 })

  const yAxis = d3.scaleLinear()
    .domain([0, d3.max(dataset, (d) => { return d.y })])
    .range([height - padding, 0])
  svg
    .append("g")
    .attr("transform", "translate(25,29)")      // This controls the vertical position of the Axis
    .call(d3.axisLeft(yAxis));



});


    // var config = { responsive: true }
    // var layout = {
    //   title: 'messages sent per user',
    //   font: {
    //     size: 17,
    //     family: 'Nunito, sans-serif'

    //   }
    // };
    // Plotly.newPlot('traces', data, layout, config);
    // var data = JSON.parse(document.getElementById("traces").getAttribute("data"));
