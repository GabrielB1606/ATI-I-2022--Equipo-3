function toggleReplies(section)
{
    var commentSection = $(section);
    var opened = commentSection.data("opened");

    if(!opened){
        commentSection.removeClass("d-none");
        commentSection.addClass("d-block");
    }
    else{
        commentSection.removeClass("d-block");
        commentSection.addClass("d-none");
    }
    
    $(section).data('opened',!opened); 
}

// Open or close comment list
function toggleComments(idx)
{
    var newComment = $("#user-new-comment-"+idx);
    var opened = $("#comment-section-"+idx).data("opened");

    console.log(idx);
    if(!opened){
        newComment.removeClass("d-none");
        newComment.addClass("d-block");
    }
    else{
        newComment.removeClass("d-block");
        newComment.addClass("d-none");
    }
    
    toggleReplies("#comment-section-"+idx);
}


$(".comment-toggle").each( (idx)=>{
    $("#comment-toggle-"+idx  ).click( () => toggleComments(idx) );
} 
);

$(".reply-toggle").each( (idx)=>{
    $("#reply-toggle-"+idx  ).click( () => toggleReplies("#reply-section-"+idx) );
} 
);