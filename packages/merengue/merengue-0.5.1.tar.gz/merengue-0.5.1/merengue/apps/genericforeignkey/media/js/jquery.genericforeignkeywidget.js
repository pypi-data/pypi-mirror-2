(function($) {
    $.fn.generic_widget = function () {
        return this.each(function () {
            var container = $(this);
            var hidden = container.find('input[type=text]').eq(0);
            var info = container.find('span.selected_content').eq(0);
            var remove = container.find('span.remove_current').eq(0);
 
            remove.find('img').click(function() {
                hidden.val("");
                info.html(name);
            });

            $(window).focus(function() {
                if ($(".selected_content").html() != '') {
                    remove.show();
                }
            });
            $(window).triggerHandler('focus');
        });
    };

    $(document).ready(function() {
        $('.relatedgenericwidget').generic_widget();
        function initial_related_text(obj){
            var obj = $(obj);
            var link = obj.parent().find('a.content_type').attr('href');
            if (link != null) {
                var index = link.indexOf('?');
                var link_new = link.substring(0, index + 1) + "content_type_id=" + obj.val();
                obj.parent().find('a').attr('href', link_new);
            }
        }
        var selects = $('select.genericforeignkey');
        $('div.obj_id').addClass('hidden');
        $('div.relatedgenericwidget a.content_type.hidden').removeClass('hidden');
        $('div.relatedgenericwidget span.selected_content.hidden').removeClass('hidden');
        for (var i=0; i<selects.length; i++){
            initial_related_text(selects[i]);
        }
        $('select.genericforeignkey').change(function(){
            $(this).parent().find('span.remove_current img').click();
            initial_related_text($(this));
        });
    });
})(jQuery);

function dismissRelatedLookupPopup(win, chosenId) {
    var name = id_to_windowname(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf("vManyToManyRawIdAdminField") != -1 &&  elem.value) { 
            elem.value += "," + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
        jQuery("#"+name).parent().parent().find("span.selected_content").html(jQuery(win.document).find("a[href="+chosenId+"/]").html());
    } 
    win.close();
}

 function gup(name, str){
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp ( regexS );
    var tmpURL = str;
    var results = regex.exec( tmpURL );
    if( results == null )
        return null;
    else
        return results[1];
}

function showRelatedObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
    href = triggeringLink.href + '&pop=1';
    } else {
    href = triggeringLink.href + '?pop=1';
    }
    if(jQuery(triggeringLink).parents().find("div.relatedgenericwidget").length != 0) {
        var a_href = jQuery(triggeringLink).attr('href');
        if ((gup('content_type_id', a_href) == "") || (gup('content_type_id', a_href) == null)) {
            alert(gettext("Select first a content type"));
            return false;
        }
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
} 
