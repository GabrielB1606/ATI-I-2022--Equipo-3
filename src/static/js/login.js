

$("form[name=login_form]").submit(function (e){
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user-login/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href="/";
            console.log(resp);
        },
        error: function(resp) {
            console.log(resp);
            $("#error").show();
        }
    });
    
    e.preventDefault();
    
});


