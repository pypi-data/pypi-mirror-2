jQuery(document).ready(function($){
    var selected_id = null;
    var selected_action = null;

    function getId(jItem){
        return jItem.get(0).id.split('-')[2];
    }

    function select(jItem){
        // add a "selected" class to the (jQuery) item
        selected_id = getId(jItem);
        $('#item-row-' + selected_id).addClass('selected');
    }

    function deselectAll(){
        // some of the target containers might be visible
        // from a previous click; hide them
        $('.move-target-container').hide();
        // likewise, there might be an element previously
        // selected for moving
        if(selected_id)
            $('#item-row-' + selected_id).removeClass('selected');
        // remove the global action variables
        selected_id = null;
        selected_action = null;
    }

    // we need to reload all the onclick handlers
    // once the table contents are reloaded (after an AJAX request)
    // so we make this a function so we can call it again
    bindClicks = function(){
        $('#item-table a').click(function(e){
            var elem = $(this);
            if(elem.hasClass('move-item')){
                return moveItem.apply(this, [e]);
            }
            else if(elem.hasClass('addlink'))
                return addLink.apply(this, [e]);
            else if(elem.hasClass('move-target'))
                return moveTarget.apply(this, [e]);
        });
    }
    bindClicks();

    moveItem = function(e){
        deselectAll();

        var item = $(this);
        select(item);
        selected_action = 'move';

        var href = 'item/' + selected_id + '/valid-targets/'
        valid_targets = $.get(href, {}, function(resp){
            var ids = resp.split(',');
            $(ids).each(function(){
                var target = $('#move-target-' + this);
                target.show();
            });
        });
        return false;
    };

    addLink = function(e){
        deselectAll();

        var item = $(this);
        select(item);
        selected_action = 'add';
        
        $('#move-target-' + selected_id).show();

        return false;
    };

    moveTarget = function(e){
        // target classes look like 'move-target <where>'
        var where = $(this).attr('class').split(' ')[1];
        var target_id = getId($(this.parentNode));
        if(selected_action == 'move'){
            var href = 'item/' + selected_id + '/move/';
            $.ajax({
                type : "POST",
                url : href,
                data : { position: where, target_id : target_id },
                success : function(data, textStatus){
                    deselectAll();
                    $('#item-table').html(data);
                    bindClicks();
                },
                error : function(request, textStatus, errorThrown){
                    deselectAll();
                    alert("Error: moving the item failed " + textStatus + ' ' + errorThrown);
                }
            });
            return false;
        }
        else{
            // selected_action should be 'add'; no assert in JS...
            var href = 'item/add/as/' + where + '/of/' + target_id + '/';
            window.location.href = href;
        }
    };

});
