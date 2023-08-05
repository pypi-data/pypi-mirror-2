(function($){
    
$(document).ready(function(){
    
    $(".visualBoxEntry").mouseenter(
        function(){
            $(this).find("img").fadeOut(560, function() {
            });
        }
    );

    $(".visualBoxEntry").mouseleave(
        function(){
            $(this).find("img").fadeIn(480, function() {
            });
        }
    );
    
});
    
})(jQuery);



