$(document).ready(function(){
  // confirm deletion of item
  $(".confirm").live("click", function(){
    message = $(this).attr('title');
      if (! message) {
        message = $(this).text();
      }
      if (! message) {
        message = "Continue";
      }
      if (! confirm(message + "?")) {
        return false;
      }
  });
});