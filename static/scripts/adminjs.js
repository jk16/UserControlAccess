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
				url: '/admin',
				data: userandpass,
				success: function(response) {
					console.log("response: " + response)
				},
				error: function(response) {
					console.log(response)
					alert('error')
				}
			})
		}

	});


});













