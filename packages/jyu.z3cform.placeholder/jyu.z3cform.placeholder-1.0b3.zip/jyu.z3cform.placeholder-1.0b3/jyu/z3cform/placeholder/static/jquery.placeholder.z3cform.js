/*globals document,$,jQuery*/
(function($){
  $.fn.placeholder_z3cform = function(options) {
    return $(this).each(function() {
      $(this).find("input[type=text]").each(function() {
        var placeholder = this.title;
        if (placeholder !== undefined && placeholder.length > 0) {
          $(this).watermark(placeholder);
        } else if ($(this).parents("div[id$=-autocomplete]").length > 0) {
          placeholder = $(this).parents("div[id$=-autocomplete]:eq(0)").attr("title");
          $(this).parents("div[id$=-autocomplete]:eq(0)")
            .attr("title", null).find("input[title]").attr("title", null);
          if (placeholder !== undefined && placeholder.length > 0) {
            $(this).watermark(placeholder);
          }
        }
      });
    });
  };
})(jQuery);

jQuery(function($) {
  $("form .field").placeholder_z3cform();
  $(".overlay-ajax").bind("onLoad", function() {
    $(this).find("form .field").placeholder_z3cform();
  });
});
