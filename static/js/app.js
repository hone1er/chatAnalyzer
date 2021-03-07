$(document).ready(function () {
  $("table").DataTable({
    pagingType: "simple",
  });
console.log(JSON.parse(document.getElementById("traces").getAttribute("data")));
var data = JSON.parse(document.getElementById("traces").getAttribute("data"));
var config = {responsive: true}
var layout = { 
  title: 'messages sent per user',
  font: {size: 17,
  family: 'Nunito, sans-serif'

  }
};
Plotly.newPlot('traces', data, layout, config);
});
