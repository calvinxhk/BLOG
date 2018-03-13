var back_to_top = $(".back-to-top");
$(window).scroll(function(){if($(document).scrollTop()>'300'){back_to_top.css("display","block")}else{back_to_top.css("display","none")}});
back_to_top.mouseover(function(){$(this).css("background-position","0px -39px")});
back_to_top.mouseout(function(){$(this).css("background-position","0px 0px")});
back_to_top.click(function(){$("html,body").animate({scrollTop:0},500)});


