$(document).ready(function() {
    $adminForm = $("#adminForm");
    $adminUser = $("#adminUser");
    $adminPass = $("#adminPass");


    $adminForm.on('submit', function(e) {
        if($adminForm.is(".userStep")) {
            e.preventDefault();
            $adminForm.removeClass("userStep");
            $adminUser.hide();
            $adminPass.show();
        }
        else {
            e.preventDefault();
            $adminPass.hide();


            userandpass = {
                user: $("#adminUser input").val(),
                pass: $("#adminPass input").val()
            };

            //post to send login data to server
            $.ajax({
                type: 'POST',
                url: '/adminCreds',
                data: userandpass,
                success: function(response) {
                    if(response.success) {
                        //get request for data, then load html
                        $.ajax({
                            type: "POST",
                            url: "/getListUsers",
                            data: {"message": }
                            success: function(response) {

                            }
                        });
                    }
                    else {

                    }
                },
                error: function(response) {
                    alert("error");
                    console.log("error --> response: " + JSON.parse(response));
                }
            });
        }

    });


});












