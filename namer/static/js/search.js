$(document).ready(function(){
    $("#search").autocomplete({
        source: function(request, response){
            $.getJSON("/api/v1/search",
            {
                term: request.term,
                limit: 24
            },
            function(data) {
                response(data.hits);
            });
        },
        minLength: 3
    });
});
