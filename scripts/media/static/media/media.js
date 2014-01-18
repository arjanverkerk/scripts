$(document).keydown(function(eventObject) {
  console.log(eventObject.which);
});

$(document).ready()
$.get( "media/" + path, function( data ) {
  $( "#media" ).html(data);
});
