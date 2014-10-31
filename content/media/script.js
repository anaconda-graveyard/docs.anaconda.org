var MAX_NAV_WIDTH = MEDIA_XS = 768; 
var MAX_IMG_ZOOM_WIDTH = MEDIA_SM = 992;

var showFullNav = function(duration){
	var navbar = $('nav.navbar');
    if (navbar.hasClass('small-nav')){
        navbar.removeClass('small-nav');
        navbar.stop();
        navbar.animate({width:'100%'}, duration, function(){
            navbar.find('.navbar-js-collapse').addClass('navbar-collapse');
            navbar.find('.navbar-header').removeClass('navbar-header-always');
        });
    }
};

var showSmallNav = function(duration){
	var navbar = $('nav.navbar');
    if ($('body').width() >= MAX_NAV_WIDTH && !navbar.hasClass('small-nav')){
        navbar.addClass('small-nav');
        navbar.find('.navbar-js-collapse').removeClass('navbar-collapse');
        navbar.find('.navbar-header').addClass('navbar-header-always');
        navbar.stop();
        navbar.animate({width:'200px'}, duration, function(){
          navbar.find('.navbar-js-collapse').removeClass('navbar-collapse');
          navbar.find('.navbar-header').addClass('navbar-header-always');
        });
    }
}

if ($(document).scrollTop() >= 50){
	showSmallNav(0);
}

document.getElementById('topNav').style.display = '';

$(window).on('scroll resize', function(e){
	if ($('body').width() < MAX_NAV_WIDTH){
		showFullNav(400);
		return;
	}
	
	if ($(document).scrollTop() < $('nav.navbar').height()){
      showFullNav(400);
	} else {
	  showSmallNav(400);
	}
});

if ($('body').width() >= MAX_IMG_ZOOM_WIDTH){
	
  
  var imgs = $('.method-example img');
  
  imgs.addClass('zoom');
  
  $('body').on('click', '#modalBG', function(){
  	$('#modalBG').hide().empty();
  });
  
  $('body').on('keyup', function(e){
  	if (e.keyCode == 27){
  	  $('#modalBG').hide().empty();
  	}
  });
  
  $('body').on('click', '.method-example img', function(e){
  	console.log('click');
  	var $img = $(e.currentTarget).clone().appendTo($('#modalBG'));
  		$img.addClass('expanded');
  		$('#modalBG').fadeIn(200);
  		$img.css('position','fixed')
  	        .css('top', ($('body').height() - $img.height())/2)
  	        .css('left', ($('body').width() - $img.width())/2);
  });
}
