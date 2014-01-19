var mime = {
  "jpg": "image",
  "ogv": "video"
}

$(document).keydown(function(eventObject) {
  var key = eventObject.which;
  console.log(key);
  switch (key) {
    case 37:
      index -= 1;
      update();
      break;
    case 39:
      index += 1;
      update();
      break;
    }
  
});

function update() {
  // validate
  if (index < 0) {
    index = length - 1;
  }
  if (index >= length) {
    index = 0;
  }
  // load
  $.get('html/' + index, function(data) {
    $(".main").html(data);
  });
}

$(document).ready(update)
