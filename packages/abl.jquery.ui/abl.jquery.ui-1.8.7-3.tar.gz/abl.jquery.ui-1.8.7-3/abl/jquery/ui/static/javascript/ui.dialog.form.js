/*
This is not a plugin.
Here you can find a default callbacks for submit.
It requires jquery.form.widget.js and
jquery.update.content.js to be loaded.
*/

//binds success as a callback on ajaxSubmit
function submit() {
    form = $('.ui-dialog form')
    opts = {success: success}
    submit_form(form, opts);
}

//Replaces some content on success and closes the
//dialog
function success(content) {
    updated = update_content(content, '.ui-dialog-content');
    if (updated == true) {
        close();
    }
    return false;
}



