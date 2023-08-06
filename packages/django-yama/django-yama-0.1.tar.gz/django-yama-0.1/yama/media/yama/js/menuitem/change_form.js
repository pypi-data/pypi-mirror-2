jQuery(document).ready(function($){
    // need to figure out our 'base' url
    // the url looks like http://blah.../menu/blah...
    var parts = window.location.href.split('/');
    var MENU_ADMIN_ROOT = parts.splice(0, parts.indexOf('menu') + 1).join('/');

    $(".object_id").append("<div id='lookup_box'/>");
    $("#id_object_id").after("<span style='padding-left: 5px; font-style: italic' id='repr_object_id'/>");

    display_lookup = function(){
        var opt = $("#id_content_type option:selected");
        var type = opt.text().toLowerCase();
        var value = opt.val();
        if(value){
            var link_root = MENU_ADMIN_ROOT + '/contenttype/';
            $("#lookup_box").html("<a onclick='return showRelatedObjectLookupPopup(this);' id='lookup_id_object_id' class='related-lookup'></a>");
            $("#lookup_id_object_id").text(gettext("Choose a ") + type);
            $("#lookup_id_object_id").attr('href', link_root + value + '/');
        }
        else
           $("#lookup_box").html('');
       $('#id_object_id').val('');
       $('#repr_object_id').html('');
    };

    // this is set as a global JS variable in the template
    if(link_object_repr){
        $('#repr_object_id').html('(' + link_object_repr + ')');
        display_lookup();
    }

    $("#id_content_type").change(display_lookup);

});

