$(document).ready(function() {
    var $adminForm = $("#AdminForm");
    var $adminUser = $("#adminUser");
    var $adminPass = $("#adminPass");
    var $firstPasswordVerification = $("#firstPasswordVerification");
    var $confirmPassVerification = $("#confirmPassVerification");

    $adminForm.on("submit", function(e){
        e.preventDefault();
        //enter password
        var firstPassSubmit = $(this).is(".passwordNotConfirmed");

        if(firstPassSubmit) {
            $(this).removeClass("passwordNotConfirmed");
            $firstPasswordVerification.hide();
            $confirmPassVerification.show();
        } 
        else {

            var password ={ password:$confirmPassVerification.val()};

            $.ajax({
                type: 'POST',
                url: '/adminCreds',
                data: password,
                success: function(response) {
                    var parsedResponse = JSON.parse(response);
                    if(parsedResponse.success) {
                        redirect('/crudpanel');
                    }
                    else {
                        redirect('/');
                    }
                }
            });

        }
    });

    $confirmPassVerification.on("keyup", function() {
        var matchingPass = $(this).val() == $firstPasswordVerification.val();
        var $matchingMessage = $(".matchingMessage");
        if(matchingPass) {
            $matchingMessage.html('matching').css('color', 'green');
        }
        else {
            $matchingMessage.html('matching').css('color', 'red');
        }
    });

});


function redirect(url){
    window.location.href = url;
}







