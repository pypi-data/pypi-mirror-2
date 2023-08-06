/*
A ui dialog that simply loads a content url
The dialog becomes visible when the response is
complete to avoid ugly style changes during
content loading.

A previous dialog gets deleted before a new dialog
will be displayed.

If no content_url is provided as a parameter the
HTML attribute href of the triggered element will be used.
If no title is provided in options the
HTML attribute title of the triggered element will be used.
*/

(function($) {
  jQuery.fn.dialog_content = function(options) {
    jQuery(this).live('click', function() {
        make_dialog(this, options);
        return false;
    });
  }
})(jQuery);

function make_dialog(elem, options) {
    //get a url if not provided as parameter
    if (!options['url']) {
        var content_url = jQuery(elem).attr('href');
    }
    else {
        var content_url = options['url'];
    }
    //get a title if provided as parameter
    if (jQuery(elem).attr('title')) {
        options['title'] = jQuery(elem).attr('title');
    }
    //prevent caching
    var timestamp = new Date().getTime();
    var arguments = '_=' + timestamp;

    separator = '?';
    if (content_url.indexOf('?') != -1) {
    separator = '&';
    }

    content_url = content_url + separator + arguments
    //first load the content, then display the dialog
    $.get(content_url, function(data) {
        var payload = jQuery(data);
        $(payload[0]).dialog(options);
        if (payload[1]) {
            //it may contain some javascript that needs to be executed
            eval($(payload[1]).html());
        }
    });
}

//A simple close function that removes the dialog
//and its content
function close() {
    //$(this).dialog('close');
    $('div.ui-widget-overlay').remove();
    $('div.ui-dialog ').remove();
}