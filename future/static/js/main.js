$(document).ready(function(){
	
	$('.commentPrompt').focus(function(){
		if (this.value == "Write a comment...") {
			$(this).css("height", "40px");
			$('.submitButton', this).css("display", "inline");
			$(this).css("color", "black");
			$(this).attr("value", "");
		}
	});
	
	$('.commentPrompt').blur(function(){
		if (this.value == ""){
			$(this).css("color", "#ccc");
			$(this).attr("value", "Write a comment...");
		}
	});

	$('.postPrompt').focus(function(){
		if (this.value == "Post new message") {
			$(this).css("height", "40px");
			$('.submitButton', this).css("display", "inline");
			$(this).css("color", "black");
			$(this).attr("value", "");
		}
	});
	


	$('.postPrompt').blur(function(){
		if (this.value == ""){
			$(this).css("color", "#ccc");
			$(this).attr("value", "Post new message");
		}
	});


	$('.content-container').click(function(event){
		var target = event.target;
		
		currentContainer = this;
		currentComment = $('.commentBox', this);
		
		if($(target).is(".action")){
			$('.commentBox', this).css("display", "block");
		}

	});
		

	$('form').keypress(function(e){
		if (e.which == 13){
			e.preventDefault();
			this.submit();
		}
	}); 
	
	

	
	$('.posttext').each(function(){
	
		function hashTagFilter(post){
			
			function linkify(match){
				return "<a href=/" + match.substring(1) + "/ class='hashtag'>" + match + "</a>";
			}
			return post.replace(/#([-_a-zA-Z0-9]{1,24})/gi, linkify); 
		}

		var val = $(this).html();
		val = hashTagFilter(val);
		$(this).html(val);	
	});
	
	$('.comment').each(function(){
	
		function hashTagFilter(post){
			
			function linkify(match){
				return "<a href=/" + match.substring(1) + "/ class='hashtag'>" + match + "</a>";
			}
		
			return post.replace(/#([-_a-zA-Z0-9]{1,24})/gi, linkify);
		
		}

		var val = $(this).html();
		val = hashTagFilter(val);
		$(this).html(val);	
	});
	
	$('.hashtag').each(function(){
	
		function hashTagFilter(post){
			
			function linkify(match){
				return "<a href=/" + match.substring(1) + "/ class='hashtag'>" + match + "</a>";
			}
		
			return post.replace(/[#]+([-_a-zA-Z0-9]+)/gi, linkify);
		
		}

		var val = $(this).html();
		val = hashTagFilter(val);
		$(this).html(val);	
	});
	
	$('.posttext').each(function(){
	
		function atFilter(post){
			
			function linkify(match){
				return "<a href=/user/" + match.substring(1) + "/ class='atMention'>" + match + "</a>";
			}
		
			return post.replace(/[@]([a-zA-Z]+)[-]([a-zA-Z]+)/gi, linkify);
		
		}

		var val = $(this).html();
		val = atFilter(val);
		$(this).html(val);	
	}); 
	
	$('.comment').each(function(){
	
		function atFilter(post){
			
			function linkify(match){
				return "<a href=/user/" + match.substring(1) + "/ class='atMention'>" + match + "</a>";
			}
		
			return post.replace(/[@]([A-Z][a-z]+)[-]([A-Z][a-z]+)/gi, linkify);
		
		}

		var val = $(this).html();
		val = atFilter(val);
		$(this).html(val);	
	}); 
	
	
	
	$('.searchBox').focus(function(){
		if (this.value == "Search") {
			$('.submitButton', this).css("display", "inline");
			$(this).css("color", "black");
			$(this).attr("value", "");
		}
	});
	
	$('.searchBox').blur(function(){
		if (this.value == ""){
			$(this).css("color", "#ccc");
			$(this).attr("value", "Search");
		}
	});
	
});
