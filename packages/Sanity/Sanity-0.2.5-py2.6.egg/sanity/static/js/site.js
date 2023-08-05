$(document).ready(function(){
    $('.tags ul li.cancel').hide();
    $('.tags ul li a').click(function(){
        $('.tags ul li.cancel').show();
        $('.tags ul li a').css('backgroundColor', '#444');
        $('.tags ul li.cancel a').css('backgroundColor', '#333');
        $(this).css('backgroundColor', '#777');
    });
    $('.tags.group ul li a').click(function(){
        $('.tasks ul').load('/tasks/group/tag/'+$(this).html());
    });
    $('.tags.progress ul li a').click(function(){
        $('.tasks ul').load('/tasks/progress/tag/'+$(this).html());
    });
    $('.tags.completed ul li a').click(function(){
        $('.tasks ul').load('/tasks/completed/tag/'+$(this).html());
    });

	setTimeout(function(){
		$("#flashes").fadeOut("slow", function () {
		$("#flashes").remove();
	}); }, 2000);	
});
