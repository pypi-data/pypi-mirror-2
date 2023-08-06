//Callbacks for autocomplete

//submit form when a suggestion was clicked
function autocomplete_select_callback(event, ui) {
    $(this).val(ui.item.label);
    $(this).parents("form").submit();
}

//submit form if a suggestion was selected and enter was pressed
function autocomplete_submit_on_enter_callback(e) {
    var keyCode = e.keyCode || e.which; if(keyCode == 13) {
    $(this).parents("form").submit();
    }
}

//Callbacks for instant search

//move the results down so they do not overlap with suggestions
function autocomplete_open_callback(event, ui) {
    var autocomplete_elems = $('ul.ui-autocomplete li')
    var autocomplete_height = autocomplete_elems.height() * autocomplete_elems.size();
    $(this).css('margin-bottom', autocomplete_height);
}


//move the results up when suggestion are closed
function autocomplete_close_callback(event, ui) {
    $(this).css('margin-bottom', 0);
    return false;
}

//a source callback that also retrieves instant search results
function autocomplete_source_callback(request, response) {
  var self = this;
    if (self.ajax_reqest) {
        self.ajax_reqest.abort();
    }
    self.ajax_reqest = $.ajax({
        url: self.instant_url,
        data: {term: request.term},
        success: function( data ) {
            var payload = $($(data)[1]);
            if (data) {
                update_content(data);
            }
            response( $.map( eval(payload.find('#instant_suggestions').html() ), function( item ) {
                return {
                    label: item,
                    value: item
                }
           }));
        }
    });
}

//get new instant results if a suggestion was selected
function autocomplete_instantsearch_select_callback(event, ui) {
    var self = this;
    if (self.ajax_reqest) {
        self.ajax_reqest.abort();
    }
    self.ajax_reqest = $.ajax({
        url: "",
        data: {
            query: ui.item.value,
            partial: 1,
            search_results_page: 1
        },
        success: function( data ) {
            if (data) {
                var cont = $('#search_results').parent().parent();
                var old_content = cont.find('.pager_content');
                var new_pager = $(data).find('.pager');
                var new_content = $(data).find('.pager_content').children();
                cont.find('.pager').html(new_pager.html());
                old_content.html(new_content);
            }
        }
    });
}

//handle selections for multiple automplete
function focus_multiple_callback() {
  // prevent value inserted on focus
  return false;
}

function multiple_autocomplete_split(val) {
  return val.split(/,\s*/);
}

function select_multiple_callback(event, ui) {
  var terms = multiple_autocomplete_split( this.value );
  // remove the current input
  terms.pop();
  // add the selected item
  terms.push(ui.item.value);
  // add placeholder to get the comma-and-space at the end
  terms.push( "" );
  this.value = terms.join(", ");
  return false;
}

function multiple_autocomplete_extract_last(term) {
  return multiple_autocomplete_split(term).pop();
  }

function multiple_autocomplete_keydown_callback(event){
  if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active) {
    event.preventDefault();
  }
}
