/* this is basically the standard Django admin js function, but we need
 * to modify it to pass it two values instead of just one (object id + repr
 * instead of just object id)
 */
function menuDismissRelatedLookupPopup(win, chosenId, chosenRepr) {
    var $ = jQuery;
    var name = win.name.replace(/___/g, '.');
    var elem = $('#' + name);
    var repr_name = name.replace(/^id_/, 'repr_');
    var repr_elem = $('#' + repr_name);

    elem.val(chosenId);
    repr_elem.html('(' + chosenRepr + ')');
    $('#id_caption').val(chosenRepr);
    win.close();
}
