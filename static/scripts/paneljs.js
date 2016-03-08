$(document).ready(function(){
    $verifyPermissionsForm = $("#verifyPermissionsForm");
    $operationToVerify = $("#operationToVerify");
    $specificToVerify = $("#specificToVerify");
    $addPermissionForm = $("#addPermissionForm");
    $operationToAdd = $("#operationToAdd");
    $specificToAdd = $("#specificToAdd");

    $verifyPermissionsForm.on("submit", function(e){
        e.preventDefault();
        var specific = $specificToVerify.val();
        var operation = $operationToVerify.val();
        var message = {
            specific: specific,
            operation: operation
        };
        $.get("/hasPerm", message, function(response){
           var parsedResponse = JSON.parse(response);
           console.log(parsedResponse.has_permission);
        });
    });

    $addPermissionForm.on("submit", function(e) {
        console.log('addPermissionForm called')
        e.preventDefault();
        var specific = $specificToAdd.val();
        var operation = $operationToAdd.val();
        var message = {
            specific: specific,
            operation: operation,
        };

        $.get("/addPerm", message, function(response){
            var parsedResponse = JSON.parse(response);
            console.log(parsedResponse);
        });
    });
});