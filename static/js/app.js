$(document).ready(function() {
    $('table').DataTable( {
      "pagingType": "simple"
  } );
  } );

  var anim = bodymovin.loadAnimation({
  container: document.getElementById("animation"),
  path: "Animation.json",
  renderer: 'svg',
  loop: true,
  autoplay: true,
});