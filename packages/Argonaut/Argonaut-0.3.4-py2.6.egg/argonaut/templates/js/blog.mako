<%def name="js()">
    <script type="text/javascript">
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
    </script>
</%def>
