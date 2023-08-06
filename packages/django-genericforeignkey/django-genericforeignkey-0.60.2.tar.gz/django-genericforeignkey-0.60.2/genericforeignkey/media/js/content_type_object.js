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
          var content_type_id = gup("content_type_id");
          $.map($("p.paginator a, div.pagination a.page," +
                  "div.pagination a.prev, div.pagination a.next," +
                  "#changelist-filter a"), function(item, i){
            $(item).attr("href", $(item).attr("href") + "&content_type_id=" + content_type_id);
          });
          $("<input type='hidden' name='content_type_id' value='" + content_type_id +"'></input>").appendTo("form#changelist-search");

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
