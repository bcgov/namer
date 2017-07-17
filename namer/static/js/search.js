$(document).ready(function(){
    $("#search").autocomplete({
        source: function(request, response){
            $.getJSON("/api/v1/search",
            {
                term: request.term,
                limit: 20
            },
            function(data) {
                response(data.hits);
            });
        },
        minLength: 3
    });
});
