var sidebarOut = true, speed = 1000, 
	sidebarWidth = 275, arrowbarWidth = 35,
	tooltipHeight = 500, screenHeight = $(window).height(),
	screenWidth = $(window).width(), screenWidthSidebar = $(window).width() - sidebarWidth - arrowbarWidth;

$(document).ready(function() {

updateSize(screenWidthSidebar, screenHeight);


//changes the image and retracts the sidebar
$('#arrow img').click(function() {
	if (sidebarOut) {
		$('#sidestream').animate({left: -1*(arrowbarWidth+sidebarWidth)}, speed);
		
		setTimeout(function(){ 
			$('#arrow img').attr('src', '/static/images/right-arrow.png');
		},1000);
		updateSize(screenWidth, screenHeight);
        sidebarOut = false;
	}
	else {
		$('#sidestream').animate({left: 0}, speed);

		setTimeout(function(){ 
	        $('#arrow img').attr('src', '/static/images/left-arrow.png');
    	},1000);
		updateSize(screenWidthSidebar, screenHeight);
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
	$('.add-game-cont').toggle();
	$('#add-game-screen').toggle();
});

$('.switchToProfile').click(function() { switchToProfile(); });
$('.switchToLobby').click(function() { switchToLobby(); });
$('.switchToGame').click(function() { switchToGame(); });
$('.switchToFriendsGames').click(function() { switchToFriendsGames(); });

function switchToProfile()
{
	if($('#game').is(":visible")){
	$('#game').fadeOut(500);
	}
	if($('#lobby').is(":visible")){
	$('#lobby').fadeOut(500);
	}
	if($('#friends-games').is(":visible")){
	$('#friends-games').fadeOut(500);
	}	
	setTimeout(function(){$('#profile').fadeIn(500);}, 500);	
}

function switchToLobby()
{
	if($('#profile').is(":visible")){
	$('#profile').fadeOut(500);
	}
	if($('#game').is(":visible")){
	$('#game').fadeOut(500);
	}
	if($('#friends-games').is(":visible")){
	$('#friends-games').fadeOut(500);
	}	
	setTimeout(function(){$('#lobby').fadeIn(500);}, 500);	
}

function switchToGame()
{
	if($('#lobby').is(":visible")){
	$('#lobby').fadeOut(500);
	}
	if($('#profile').is(":visible")){
	$('#profile').fadeOut(500);
	}
	if($('#friends-games').is(":visible")){
	$('#friends-games').fadeOut(500);
	}	
	setTimeout(function(){$('#game').fadeIn(500);}, 500);
}

function switchToFriendsGames()
{
	if($('#lobby').is(":visible")){
	$('#lobby').fadeOut(500);
	}
	if($('#profile').is(":visible")){
	$('#profile').fadeOut(500);
	}
	if($('#game').is(":visible")){
	$('#game').fadeOut(500);
	}	
	setTimeout(function(){$('#friends-games').fadeIn(500);}, 500);
}

function updateSize(width, height){
	$('#profile').height(height);	
	$('#lobby').height(height);	
	$('#game').height(height);
	$('#friends-games').height(height);	
	$('#profile').animate({width: width}, speed);
	$('#lobby').animate({width: width}, speed);
	$('#game').animate({width: width}, speed);
	$('#friends-games').animate({width: width}, speed);
}

});

$(window).resize(function() {
screenHeight = $(window).height();
screenWidth = $(window).width();
screenWidthSidebar = $(window).width() - sidebarWidth - arrowbarWidth;
$('#search-field').height(screenHeight);
if(!sidebarOut){
	$('#profile').width(screenWidth);	
	$('#lobby').width(screenWidth);	
	$('#game').width(screenWidth);
	$('#friends-games').width(screenWidth);		
}
else{
	$('#profile').width(screenWidthSidebar);	
	$('#lobby').width(screenWidthSidebar);	
	$('#game').width(screenWidthSidebar);
	$('#friends-games').width(screenWidthSidebar);		
}
});