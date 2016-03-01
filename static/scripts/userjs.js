$(document).ready(function() {
    var $registerUserBtn = $("#registerUserBtn");
    var $notRegisteredPanel = $("#notRegisteredPanel");
    var $enterPass = $("#enterPass");
    var $firstPasswordRegister = $("#firstPasswordRegister");
    var $confirmPassRegister = $("#confirmPassRegister");
    var $RegisterUserForm = $("#RegisterUserForm");
    var $IsRegisteredForm = $("#IsRegisteredForm");
    var $firstPasswordVerification = $("#firstPasswordVerification");
    var $confirmPassVerification = $("#confirmPassVerification");
    //user does not exist, register password
    $registerUserBtn.click(function() {
        $notRegisteredPanel.hide();
        $enterPass.show();
    });
    //user exists, login
    $IsRegisteredForm.on("submit",function(e){
        e.preventDefault();
        var user = window.location.pathname;
        user = user.replace('/', '');
        //enter password
        var firstPassSubmit = $(this).is(".passwordNotConfirmed");

        if(firstPassSubmit) {
            $(this).removeClass("passwordNotConfirmed");
            $firstPasswordVerification.hide();
            $confirmPassVerification.show();
        }
        else {
            var password = {
                userName: user,
                password: $confirmPassVerification.val()
            };

            $.ajax({
                type: 'POST',
                url: '/verifyPassword',
                data: password,
                success: function(response) {
                    // alert('verify')
                    parsedResponse = JSON.parse(response);
                    if(parsedResponse.success) {
                        var page = "/"+user + "/panel";
                        redirect(page);
                    }
                }
            });

        }
    });



    $RegisterUserForm.on("submit", function(e){
        e.preventDefault();
        // if user entered the first password remove .passwordNotConfirmed
        var firstPassSubmit = $(this).is(".passwordNotConfirmed");
        if(firstPassSubmit) {
            $(this).removeClass("passwordNotConfirmed");
            $confirmPassRegister.hide();
            $confirmPassRegister.show();
        }
        //submit and does not contain .passwordNotConfirmed
        else {
            //user is submitting password
            //add a POST
            var password = {password: $confirmPassRegister.val()};
            $.ajax({
                type: 'POST',
                url: '/registerPassword',
                data: password,
                success: function(response) {
                    response = JSON.parse(response);
                    if(response.success) {
                        //redirect to success
                        var page = "/"+response.userName + "/panel";
                        redirect(page);
                    }
                    else {
                        //redirect to fail
                    }
                }
            });
            //on success promt to a new page
        }
    });

    $confirmPassRegister.on("keyup", function() {
        var matchingPass = $(this).val() == $firstPasswordRegister.val();
        var $matchingMessage = $(".matchingMessage");
        if(matchingPass) {
            $matchingMessage.html('matching').css('color', 'green');
        }
        else {
            $matchingMessage.html('matching').css('color', 'red');
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