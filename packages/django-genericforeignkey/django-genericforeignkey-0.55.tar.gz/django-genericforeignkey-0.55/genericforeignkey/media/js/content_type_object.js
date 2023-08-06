(function($) {
    $(document).ready(function () {
            function gup( name ){
                var regexS = "[\\?&]"+name+"=([^&#]*)";
                var regex = new RegExp ( regexS );
                var tmpURL = window.location.href;
                var results = regex.exec( tmpURL );
                if( results == null )
                    return null;
                else
                    return results[1];
            }
          $.map($("p.paginator a, div.pagination a.page, div.pagination a.prev, div.pagination a.next"), function(paginate, i){
            $(paginate).attr("href", $(paginate).attr("href") + "&content_type_id=" + gup("content_type_id"));
          });
          $("form table tr th a").click(function() {
            if (gup("content_type_id") != null){
                return false;
            }
            else {
                var content_type_id = $(this).attr("href").replace("/", "");
                var location_href = window.location.href;
                if (location_href.indexOf("?") == -1){
                    location_href += "?";
                }
                document.location.href = location_href + "&content_type_id="+ content_type_id;
                return false;
            }
          });
 
        });
})(jQuery);
