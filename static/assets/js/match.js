jQuery(document).ready(function($) {
    $(".clickable").css('cursor', 'pointer');
    $(".clickable").click(function() {
        window.document.location = $(this).data("href");
    });
});