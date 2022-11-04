function selectChat(id_contact) {
    
    $(".contact").css("background-color", "white");
    $("#"+id_contact).css("background-color", "#eee");

    $( "#chat-div-container" ).removeClass("d-none");
    $( "#chat-div-container" ).addClass("d-block");

    $(".messageList").removeClass("d-block");
    $(".messageList").addClass("d-none");

    let chat_element = $( "#chat-"+ id_contact );
    chat_element.removeClass("d-none");
    chat_element.addClass("d-block");
    chat_element.scrollTop( chat_element.height() );

}

$(".contact").each( (idx)=>{
        let id_contact = $(".contact")[idx].id;
        console.log( id_contact ) ;
        $("#"+id_contact ).click( () => selectChat(id_contact) );
    } 
);
