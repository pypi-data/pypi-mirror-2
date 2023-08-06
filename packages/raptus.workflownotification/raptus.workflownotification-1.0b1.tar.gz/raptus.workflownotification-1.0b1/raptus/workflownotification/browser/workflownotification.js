(function($) {
  $(document).ready(function() {
    $('#plone-contentmenu-workflow dd.actionMenuContent a.workflownotification').click(function(e) {
      e.preventDefault();
      $.get($(this).attr('href').replace('workflownotification_form', 'workflownotification_form-ajax'), {}, function(data) {
        $('#js-workflownotification_form-overlay').remove();
        $('#js-workflownotification_form').remove();
        $('body').append(data);
        $('body').append('<div id="js-workflownotification_form-overlay"></div>');
        $('#js-workflownotification_form input[name=form.actions.label_cancel], #js-workflownotification_form-overlay').click(function(e) {
          e.preventDefault();
          $('#js-workflownotification_form-overlay').fadeOut('fast');
          $('#js-workflownotification_form').fadeOut('fast');
        });
      })
    });
  })
})(jQuery);
