$("#searchbar-users").on("input", e =>{
    if( e.target.value.length === 0 ){
        $("#search-preview").css("visibility", "hidden");
    }else{
        $("#search-preview").css("visibility", "visible");
    }
} );

$("#search-preview").css("visibility", "hidden");