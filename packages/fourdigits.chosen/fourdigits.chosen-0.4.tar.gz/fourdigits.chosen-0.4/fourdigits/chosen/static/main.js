;(function ($) {
    $(function(){
        /* Apply to document */
        $('select').chosen();

        /* Apply to popup forms */
        $(document).bind('loadInsideOverlay', function(e){
            $('select', $(this)).chosen();
        });
    });
}(jQuery));
