$(document).ready(function(){
    $permissionsForm = $("#permissionsForm");
    $operationField = $("#operationField");
    $specificField = $("#specificField");


    $permissionsForm.on("submit", function(e){
        e.preventDefault();
        var specific = $specificField.val();
        var operation = $operationField.val();
        var message = {
            specific: specific,
            operation: operation
        };
        $.get("/hasPerm", message, function(response){
           var parsedResponse = JSON.parse(response);
           alert(parsedResponse.has_permission)
        });
    });
});