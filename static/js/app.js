$(document).ready(function () {

    createBars()
    $("table").DataTable({
      pagingType: "simple",
    });

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


function createBars() {
  setTimeout(() => {
    var data = JSON.parse(document.getElementById("traces").getAttribute("data"));
    console.log(data)
    var width = 970;
    var height = 350;
    var padding = 30;
    var margin = 135;
    var adj = 20;
    // we are appending SVG first
    var svg = d3
      .select("#viz")
      .append("svg")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr(
        "viewBox",
        "-" + adj + " -" + adj + " " + (width + adj) + " " + (height + adj)
      )
      .style("margin", "auto")
      .classed("svg-content", true);
  
    //-----------------------DATA PREPARATION------------------------//
    var dataset = data;
    const yScale = d3
      .scaleLinear()
      .domain([
        0,
        d3.max(dataset, (d) => {
          return d.y;
        }),
      ])
      .range([0, height - padding]);
  // bars
    svg
      .selectAll("rect")
      .data(dataset)
      .enter()
      .append("rect")
      .attr("x", (d, i) => {
        return (i * width) / dataset.length + padding;
      })
      .attr("y", (d) => {
        return height - yScale(d.y) - padding;
      })
      .attr("height", (d) => {
        return yScale(d.y);
      })
      .attr("width", width / dataset.length - (padding + margin))
      .attr("class", "bar")
      .append("title")
      .text((d) => {
        return "name: " + d.x + "\n" + "messages sent: " + d.y;
      });
  // tool tip
    svg
      .selectAll("text")
      .data(dataset)
      .enter()
      .append("text")
      .text((d) => {
        return d.x + ": \n" + d.y;
      })
      .attr("x", (d, i) => {
        return (
          (i * width) / dataset.length +
          (width / dataset.length - (padding + margin)) / 2 -
          15
        );
      })
      .attr("y", (d) => {
        return height;
      })
      .style("font-size", "1.25rem");
  
    // title
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", -8)
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .style("text-decoration", "underline")
      .text("total messages sent");
  
    // x axis
    const yAxis = d3
      .scaleLinear()
      .domain([
        0,
        d3.max(dataset, (d) => {
          return d.y;
        }),
      ])
      .range([height - padding, 0]);
  
    svg
      .append("g")
      .attr("transform", "translate(25, 0)") // This controls the vertical position of the Axis
      .call(d3.axisLeft(yAxis));
  
    var xScale = d3.scaleLinear().domain([]).range([25, 900]);
  
    var xAxis = d3.axisBottom(xScale);
  
    svg
      .append("g")
      .attr("transform", "translate(0," + (height - padding) + ")")
      .call(xAxis);

    d3.select(".tables")
      .style("display", "flex")
  }, 0);

};