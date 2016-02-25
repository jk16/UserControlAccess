$(document).ready(function() {
    var $registerPassword = $("#register");
    var $notRegPanel = $("#notRegPanel");
    var $enterPass = $("#enterPass");
    var $firstPassword = $("#firstPassword");
    var $confirmPass = $("#confirmPass");
    var $userForm = $("#userForm");
    //user does not exist, register password
    $registerPassword.click(function() {
        $notRegPanel.hide();
        $enterPass.show();
    });

    $userForm.on("submit", function(e){
        // if user entered the first password remove .passwordNotConfirmed
        if($(this).is(".passwordNotConfirmed")) {
            e.preventDefault();
            $(this).removeClass(".passwordNotConfirmed");
            $firstPassword.hide();
            $confirmPass.show();
        }
        //submit and does not contain .passwordNotConfirmed
        else {
            //user is submitting password
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