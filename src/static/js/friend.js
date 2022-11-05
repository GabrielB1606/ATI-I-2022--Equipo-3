// Follow or Unfollow
function toggleFollow()
{
    var follow = $("#friend-request").data("follow");

    if(!follow){
        $("follow").removeClass("d-inline");
        $("#follow").addClass("d-none");

        $("#unfollow").addClass("d-inline");
        $("#unfollow").removeClass("d-none");
    }
    else{
        $("#unfollow").removeClass("d-inline");
        $("#unfollow").addClass("d-none");

        $("#follow").addClass("d-inline");
        $("#follow").removeClass("d-none");
    }
    
    $("#friend-request").data("follow",!follow); 
}

$("#friend-request").click( () => toggleFollow() );