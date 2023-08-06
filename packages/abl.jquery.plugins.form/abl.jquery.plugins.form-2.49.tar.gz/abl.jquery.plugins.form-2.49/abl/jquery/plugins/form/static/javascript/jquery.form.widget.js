/**
 * Copyright (c) 2009 ableton.com (robert.feldbinder at ableton.com)
 * Licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 *
 * A plugin that binds a form to be send via Ajax
 * The update target is the form container.
 *
 * Typical ajaxForm options can be defined.
 * See: http://jquery.malsup.com/form
 *
 * It requires the jquery.form.js to be loaded
* **/
(function($) {
  $.fn.ajax_form = function(options) {
      var defaults = {target: $(this).parent(),
                      beforeSubmit: before_submit};
      var opts = $.extend(defaults, options);
      var form = $(this);
      form.ajaxForm(opts);
  }
})(jQuery);


// the function that can be used before an
// ajaxForm is submited
function before_submit(formData, form, opts) {
  remove_hidden(form);
  block_ui(form);
}

// the function that makes the submit
// binds the form and uses the given option
function submit_form(form, opts) {
  remove_hidden(form);
  block_ui(form);
  form.ajaxSubmit(opts);
}

//A fix for GrowingFormFieldRepeater
function remove_hidden(form) {
  form.find('div.grow_form_elem:hidden').remove();
}

//Blocks the UI and displays a waiting symbol
function block_ui(form) {
  $.blockUI.defaults.overlayCSS = {};
  $.blockUI.defaults.css = {};
  form.block({message: '<div class="icon_loading" /><h1>Please wait ...</h1>'});
}

//Replaces some content on success
//See jquery.update.content.js
function submit_success(content) {
    update_content(content);
    return false;
}