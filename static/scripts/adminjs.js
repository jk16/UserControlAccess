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
	});


});













