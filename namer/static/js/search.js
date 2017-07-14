$(document).ready(function(){
    $("#search").autocomplete({
        source: function(request, response){
            $.getJSON("/api/v1.0/search", request, function(data) {
                response(data.hits);
            });
        },
        minLength: 2
    });
});
