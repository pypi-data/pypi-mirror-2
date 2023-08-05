$(document).ready(function () {	
    $('.main-top-nav-item').hover(
	function () {
	    //show its submenu
	    $(this).children('ul').fadeIn('fast');
	}, 
	function () {
	    //hide its submenu
	    $(this).children('ul').fadeOut('fast');	    
	}
    );

    $('.main-nav-item').hover(
	function () {
	    //show its submenu
	    $(this).children('ul').fadeIn('fast');
	}, 
	function () {
	    //hide its submenu
	    $(this).children('ul').fadeOut('fast');	    
	}
    );

});
