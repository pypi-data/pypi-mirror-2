 
$(document).ready(function(){
 
$(document).ready(function(){
    
    $('.visualBoxEntry').mouseover(function() {
        $(this).find("img").animate({
            opacity: 0,
            top:  '-180',
           }, 750, "swing", function() {
          $(this).hide();
       });
    });
    
    $('.visualBoxEntry').mouseleave(function() {
        $(".visualBoxEntry img").show( function() {
        $(this).animate({
            opacity: 0.95,
            top:  '0',
           }, 290, "linear");
        });
    });
    });
})(jQuery);
