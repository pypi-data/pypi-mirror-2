(function($){
    
$(document).ready(function(){
    
    $('.visualBoxEntry').mouseenter(function() {
        $(this).find("img").animate({
            opacity: 0,
            top:  '-180',
           }, 750, "swing", function() {
          $(this).find("img").hide();
       });
    });
    
    $('.visualBoxEntry').mouseleave(function() {
        $(this).find("img").show(0, function() {
        $(this).animate({
            opacity: 0.95,
            top:  '0',
           }, 290, "linear");
        });
    });

  });
})(jQuery);
