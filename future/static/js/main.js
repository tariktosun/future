$(document).ready(function(){
	var currentComment = false;

	$('.postPrompt').focus(function(){
		if (this.value == "Post new message") {
			$('textarea').css("height", "40px");
			$('.submitButton').css("display", "inline");
			$('textarea').css("color", "black");
			$('textarea').attr("value", "");
		}
	});
	
	/*$('textarea').blur(function(){
	   if (this.value == "") {
			$('textarea').css("height", "20px");
			$('.submitButton').css("display", "none");
			$('textarea').css("color", "#ccc");
			$('textarea').attr("value", "Post new message");
		}
	});*/

	$('.content-container').click(function(event){
		var target = event.target;
		/*if(currentComment!=false && currentContainer != this){
			currentComment.css("display", "none");
		
		} */
		
		currentContainer = this;
		currentComment = $('.commentBox', this);
		
		if($(target).is(".action")){
			$('.commentBox', this).css("display", "block");
		}

	});
	
	/*$('.content-container').hover(function(){
		$(this).css("background", "#f2f2f2");
	
	}, function(){
		$(this).css("background", "none");
	
	}); */
	

	$('form').keypress(function(e){
		if (e.which == 13){
			e.preventDefault();
			this.submit();
		}
	}); 
	
	

	
});
