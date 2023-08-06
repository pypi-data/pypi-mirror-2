// anti-spam idea from http://gatekiller.co.uk/Post/JavaScript_Captcha  (c) Stephen Hill
var antiSpam = function() {
    var localCounter = 0;
    if (document.getElementById("antiSpam")) {
        var a = document.getElementById("antiSpam");
        var button = document.getElementById("comment_submit");
        if (isNaN(a.value) == true) {
                a.value = 0;
        } else {
            a.value = parseInt(a.value) + 1;
            localCounter = a.value;
            // submit button is disabled by default. when countdown is finished, enable it
            if (a.value == 3) {
                $('input[type="submit"]').removeAttr('disabled');
            }
        }
    }
    var counter = setTimeout("antiSpam()", 1000);
    // cancel counting after time has passed
    if (localCounter > 3) {
        clearTimeout(counter);
    }
}
antiSpam();

// functionality when document has been loaded
$(document).ready(function() {
    // hides the comment form as soon as the DOM is ready
    // (a little sooner than page load)
    $('.post_comment').hide();
    $('.comments').hide();
    $('.ajax_loading').hide();
    
    // big thanks to http://www.learningjquery.com/2007/02/more-showing-more-hiding/comment-page-2#comment-19420
    // toggle the next div after the current p
    $('a.comment_form_expand').click(function() {
        $(this).parents('p:first').next('div.post_comment').slideToggle("slow");
        return false;
    });
    
    // load comments and unhide the comments box
    $('a.comments_expand').click(function() {
        $(this).parents('p:first').next('div').next('div').slideToggle("fast");
        $(this).parents('p:first').next('div').next('div').children("div").next().show();
        $(this).parents('p:first').next('div').next('div').children("div:first").load($(this).parents('p:first').next('div').next('div').next('div').html(), function() {
            $(this).next('div').hide();
        });
        return false;
    });         
});
