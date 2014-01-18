var mime = {
  "jpg": "image",
  "ogv": "video"
}

$(document).keydown(function(eventObject) {
  console.log(eventObject.which);
});

function update() {
  var loc = window.location.pathname
  var ext = loc.match(/[^\.]*$/)[0]
  console.log(ext)
  var url = loc.replace("media", mime[ext.toLowerCase()])
  console.log(url)
  $.get(url, function(data) {
    $("#media").html(data);
  });
  
}

$(document).ready(update)
