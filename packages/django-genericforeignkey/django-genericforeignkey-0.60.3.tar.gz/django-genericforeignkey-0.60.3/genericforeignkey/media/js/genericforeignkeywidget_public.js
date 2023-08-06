(function($) {
    $(document).ready(function() {
        $("a.content_type").click(function(){
            var a_href = $(this).attr('href');
            if ((gup('content_type_id', a_href) == "") || (gup('content_type_id', a_href) == null)) {
                alert(gettext("Select first a content type"));
                return false;
            }
            var name = this.id.replace(/^lookup_/, '');
            name = id_to_windowname(name);
            var win = window.open(a_href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
            win.focus();
            return false;
        });

    });
})(jQuery);

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

function id_to_windowname(text) {
    text = text.replace(/\./g, "__dot__");
    text = text.replace(/\-/g, "__dash__");
    return text;
}