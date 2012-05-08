$(document).ready(function(){

/*	jQuery.fn.extend({
insertAtCaret: function(myValue){
  return this.each(function(i) {
    if (document.selection) {
      //For browsers like Internet Explorer
      this.focus();
      sel = document.selection.createRange();
      sel.text = myValue;
      this.focus();
    }
    else if (this.selectionStart || this.selectionStart == '0') {
      //For browsers like Firefox and Webkit based
      var startPos = this.selectionStart;
      var endPos = this.selectionEnd;
      var scrollTop = this.scrollTop;
      this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
      this.focus();
      this.selectionStart = startPos + myValue.length;
      this.selectionEnd = startPos + myValue.length;
      this.scrollTop = scrollTop;
    } else {
      this.value += myValue;
      this.focus();
    }
  })
}
});
	*/
	
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
	
	

	
	$('.posttext').each(function(){
	
		function hashTagFilter(post){
			
			function linkify(match){
				return "<a href=/" + match.substring(1) + "/ class='hashtag'>" + match + "</a>";
			}
		
			//get the posthash
			//var reg = /[#]+([-_a-zA-Z0-9]+)/;
			return post.replace(/[#]+([-_a-zA-Z0-9]+)/gi, linkify);
		
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
		
			//get the posthash
			//var reg = /[#]+([-_a-zA-Z0-9]+)/;
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
		
			//get the posthash
			//var reg = /[#]+([-_a-zA-Z0-9]+)/;
			return post.replace(/[@]+([-_a-zA-Z0-9]+)/gi, linkify);
		
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
