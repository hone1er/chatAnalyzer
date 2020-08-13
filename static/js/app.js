$(document).ready(function () {
  $("table").DataTable({
    pagingType: "simple",
  });
console.log(JSON.parse(document.getElementById("traces").getAttribute("data")));
var data = JSON.parse(document.getElementById("traces").getAttribute("data"));
var config = {responsive: true}
var layout = { 
  title: 'Number of messages sent per user',
  font: {size: 18}
};
Plotly.newPlot('traces', data, layout, config);
});
