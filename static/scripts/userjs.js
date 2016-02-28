$(document).ready(function() {
    var $registerUserBtn = $("#registerUserBtn");
    var $notRegisteredPanel = $("#notRegisteredPanel");
    var $enterPass = $("#enterPass");
    var $firstPassword = $("#firstPassword");
    var $confirmPass = $("#confirmPass");
    var $userForm = $("#userForm");
    //user does not exist, register password
    $registerUserBtn.click(function() {
        $notRegisteredPanel.hide();
        $enterPass.show();
    });
    //user exists, login
    $("#IsRegisteredForm").on("submit",function(e){
        e.preventDefault();

        //enter password
        var enteredPassword = $("#registeredPasswordVerification").val();

        var message = {password: enteredPassword};
        $.ajax({
            type: 'POST',
            url: '/verifyPassword',
            data: message,
            success: function(response) {
                parsedResponse = JSON.parse(response);
                console.log(parsedResponse);
            }
        });


    });



    $userForm.on("submit", function(e){
        e.preventDefault();
        // if user entered the first password remove .passwordNotConfirmed
        if($(this).is(".passwordNotConfirmed")) {
            $(this).removeClass("passwordNotConfirmed");
            $firstPassword.hide();
            $confirmPass.show();
        }
        //submit and does not contain .passwordNotConfirmed
        else {
            //user is submitting password
            //add a POST
            var password = {password: $confirmPass.val()};
            $.ajax({
                type: 'POST',
                url: '/registerPassword',
                data: password,
                success: function(response) {
                    response = JSON.parse(response);
                    $(this).hide();
                    console.log(response.success);
                    var welcome_user_html = '';
                    if(response.success === true) {
                        //idk what to do yet
                        $.get("/",function(data) {

                        });
                    }
                    else {
                        alert('false')
                        welcome_user_html = "<span>User Not Registered!</span>";
                        $enterPass.append(welcome_user_html);
                    }
                }
            });
            //on success promt to a new page
        }
    });

    $confirmPass.on("keyup", function() {
        var matchingPass = $(this).val() == $firstPassword.val();
        var $matchingMessage = $("#matchingMessage");
        if(matchingPass) {
            $matchingMessage.html('matching').css('color', 'green');
        }
        else {
            $matchingMessage.html('matching').css('color', 'red');
        }
    });



});