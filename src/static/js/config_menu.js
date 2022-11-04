// all sub-sections in the menu
let submenus = ["security", "profile", "notification", "language"];

// on click interaction function
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

// assign on click to each menu element
submenus.forEach(
    submenu => {
        $("#menu-"+submenu+"-mb").click( () => activateSubMenu(submenu) );
        $("#menu-"+submenu).click( () => activateSubMenu(submenu) );
    }
)