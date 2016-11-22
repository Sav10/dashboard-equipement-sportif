$(document).ready(function() {
	$('.box').hide();
	$('.clickme').each(function() {
	    $(this).show(0).on('click', function(e) {
	        e.preventDefault();
	        $(this).next('.box').slideToggle('fast');
	    });
	});
});
