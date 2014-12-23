$(document).ready(function() {

	$('.menu-button').click(function() {
		toggleNav();
	});

	function toggleNav() {
		if($('.content').hasClass('show-nav')) {
			$('.content').removeClass('show-nav');
		}
		else {
			$('.content').addClass('show-nav');
		}
	}

});