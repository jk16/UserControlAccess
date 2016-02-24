$(document).ready(function() {
	$adminForm = $("#adminForm");
	$adminUser = $("#adminUser");
	$adminPass = $("#adminPass");


	$adminForm.on('submit', function(e) {

		if(isUserNameSubmitted) {
			e.preventDefault();

			$adminUser.hide();
			$adminPass.show();
		}
	});


});













