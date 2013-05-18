function toggle(){
  console.log('toggle');
  var cb = $('#checkbox')
  cb.attr("checked", !cb.attr("checked"));
}
$(document).on('keydown', null, 'l', toggle);

$(document).ready(function() {
  $('.edit').editable('/', {
    type     : 'textarea', // If text, it does not make it explicit.
    indicator: 'Saving...',
    tooltip  : 'Click to edit...',
    style    : 'inherit',
  });
});
