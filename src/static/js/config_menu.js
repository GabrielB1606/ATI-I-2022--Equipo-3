let submenus = ["security", "profile", "notification", "language"];

function activateSubMenu( submenu_name ) {

    submenus.forEach(
        submenu => {
            $("#menu-"+submenu+"-mb").removeClass("active");
            $("#menu-"+submenu).removeClass("active");
            $("#"+submenu).removeClass("active");
        }
    )

    $("#menu-"+submenu_name+"-mb").addClass("active");
    $("#menu-"+submenu_name).addClass("active");
    $("#"+submenu_name).addClass("active");
    
}

submenus.forEach(
    submenu => {
        $("#menu-"+submenu+"-mb").click( () => activateSubMenu(submenu) );
        $("#menu-"+submenu).click( () => activateSubMenu(submenu) );
    }
)