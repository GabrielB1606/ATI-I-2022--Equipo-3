// Open or close comment list
function toggleComments(idx)
{
    var commentSection = $("#comment-section-"+idx);
    var opened = commentSection.data("opened");

    if(!opened){
        commentSection.removeClass("d-none");
        commentSection.addClass("d-block");
    }
    else{
        commentSection.removeClass("d-block");
        commentSection.addClass("d-none");
    }
    
    $("#comment-section-"+idx).data('opened',!opened); 
}

$(".comment-toggle").each( (idx)=>{
    $("#comment-toggle-"+idx  ).click( () => toggleComments(idx) );
} 
);