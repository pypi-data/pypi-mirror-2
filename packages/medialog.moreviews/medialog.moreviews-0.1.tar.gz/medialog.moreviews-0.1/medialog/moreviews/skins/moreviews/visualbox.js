(function($){
    
$(document).ready(function(){
    
    $(".visulBoxEntry").mouseenter(
        function(){
            $(this).find("img").fadeOut(560, function() {
            });
        }
    );

    $(".visulBoxEntry").mouseleave(
        function(){
            $(this).find("img").fadeIn(480, function() {
            });
        }
    );
    
});
    
})(jQuery);



