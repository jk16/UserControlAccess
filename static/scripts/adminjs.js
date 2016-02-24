$(document).ready(function() {
	$adminUserForm = $("#adminUserForm");
	$adminPassForm = $("#adminPassForm");


	$adminUserForm.on('submit', function(e) {
		
		e.preventDefault();

		$adminUser.hide();
		$adminPassForm.show();
	});


});













