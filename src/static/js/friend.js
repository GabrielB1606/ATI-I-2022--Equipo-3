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

// Send chat request or sent chat request
function toggleChatRequest()
{
    var sent = $("#chat-request").data("sent");

    if(sent){
        $("#sent-request-span").removeClass("d-inline");
        $("#sent-request-span").addClass("d-none");

        $("#make-request-span").addClass("d-inline");
        $("#make-request-span").removeClass("d-none");
    }
    else{
        $("#make-request-span").removeClass("d-inline");
        $("#make-request-span").addClass("d-none");

        $("#sent-request-span").addClass("d-inline");
        $("#sent-request-span").removeClass("d-none");
    }
    
    $("#chat-request").data("sent",!sent); 
}

$("#friend-request").click( () => toggleFollow() );
$("#chat-request").click( () => toggleChatRequest() );