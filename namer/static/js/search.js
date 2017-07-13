 $( function() {
    $( "#search" ).autocomplete({
        source: "/search",
        minLength: 2
    });
  } );