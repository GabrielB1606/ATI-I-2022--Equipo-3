$("#searchbar-users").on("input", e =>{
    if( e.target.value.length === 0 ){
        $("#search-preview").css("visibility", "hidden");
    }else{

        fetch(
            "/user/search/"+e.target.value,
            {
                method: 'GET',
                headers: {
                'Accept': 'application/json',
                }
            })
        .then( r => r.json())
        .then( r =>{ 
            $(".search-prev").remove();
            console.log(r);
            for( let user of r ){
                $("#search-preview").prepend(
                    `
                    <a href="user/${user.email}">
                        <li class="search-prev dropdown-item py-0 my-0">
                            <div class="userSearch d-flex mt-3 align-items-center">
                                <img alt="${user.name}" class="rounded-circle" src="${user.img_url}" width="72px" height="72px">
                                <div class="container">
                                    <strong class="d-block big">  
                                        <a href="user/${user.email}"> ${user.nombre} </a>
                                    </strong>
                                </div>
                            </div>
                        </li>
                    </a>
                    `
                )
            }    
        });

        $("#search-preview").css("visibility", "visible");
    }
} );

$("#search-preview").css("visibility", "hidden");