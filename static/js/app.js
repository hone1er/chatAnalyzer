$(document).ready(function () {
  $("table").DataTable({
    pagingType: "simple",
  });
console.log(JSON.parse(document.getElementById("traces").getAttribute("data")));
var data = JSON.parse(document.getElementById("traces").getAttribute("data"));
var config = {responsive: true}
var layout = { 
  title: 'Messages sent per user',
  font: {size: 17}
};
Plotly.newPlot('traces', data, layout, config);
});
