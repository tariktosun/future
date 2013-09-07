var sidebarOut = true, speed = 1000, 
	sidebarWidth = 275, arrowbarWidth = 35,
	tooltipHeight = 500, screenHeight = $(window).height(),
	screenWidth = $(window).width(), screenWidthSidebar = $(window).width() - sidebarWidth - arrowbarWidth;

$(document).ready(function() {

$('#search-field').height(screenHeight);
$('#search-field').width(screenWidthSidebar);

//changes the image and retracts the sidebar
$('#arrow img').click(function() {
	if (sidebarOut) {
		$('#sidestream').animate({left: -1*(arrowbarWidth+sidebarWidth)}, speed);
		
		setTimeout(function(){ 
			$('#arrow img').attr('src', '/static/images/right-arrow.png');
		},1000);
		$('#search-field').animate({width: screenWidth}, speed);
        sidebarOut = false;
	}
	else {
		$('#sidestream').animate({left: 0}, speed);

		setTimeout(function(){ 
	        $('#arrow img').attr('src', '/static/images/left-arrow.png');
    	},1000);
    	$('#search-field').animate({width: screenWidthSidebar}, speed);
        sidebarOut = true;
	}
});

//when the mouse hovers near the edge of the screen bring out the arrow
$('#arrow-hover').mouseenter(  
  function () {
  	if(!sidebarOut){
	$('#sidestream').stop().animate({left: -1*sidebarWidth}, speed);  
	$('#arrow-hover').hide();
	}
  });

//retract arrow if the user doesn't want it
$('#arrow').mouseleave(  
  function () {
  	if(!sidebarOut){
	$('#sidestream').stop().animate({left: -1*(arrowbarWidth+sidebarWidth)}, speed);
	$('#arrow-hover').show();
	}
});

//More information window
$('.card').click(function() {
	if($('.active')[0] != this){
	if($('.active')[0]){
		$('.active').find(">:first-child").hide();
		$('.active').removeClass('active');
	}
		$(this).addClass('active');
		if(screenHeight > 500){
			if(screenHeight - $(this).offset().top > 250){
				$(this).find(">:first-child").css("top", $(this).offset().top - tooltipHeight/2  + 25+ "px");		
			}
			else{	
				$(this).find(">:first-child").css("top", screenHeight - 500 + "px");
			}
		}
		$(this).find(">:first-child").toggle();
	}
	else{
		$('.active').find(">:first-child").hide();
		$('.active').removeClass('active');
	}
});

//More information window
$('#add-game-button').click(function() {
	$('#add-game-screen').toggle();
});


});

$(window).resize(function() {
screenHeight = $(window).height();
screenWidth = $(window).width();
screenWidthSidebar = $(window).width() - sidebarWidth - arrowbarWidth;
$('#search-field').height(screenHeight);
if(!sidebarOut){
$('#search-field').width(screenWidth);
}
else{
$('#search-field').width(screenWidthSidebar);	
}
});