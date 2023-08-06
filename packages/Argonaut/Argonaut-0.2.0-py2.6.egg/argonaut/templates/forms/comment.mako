<%def name="comment_form(post)">
    <div id="comment_main">
        <p>
        <%
            comment_count = h.comment.get_post_comment_count(post.id)
            if comment_count > 0:
                context.write('<a href="#" class="comments_expand">View '+str(comment_count)+' comments</a>')
            else:
                context.write('No comments')
            context.write(' (<a href="#" class="comment_form_expand">post a comment</a>)')
        %>
        </p>
        <div class="post_comment">
            <h2>Write a comment</h2><br>
            ${h.form(h.url(controller='comment', action='submit'), method='post')}
            <table>
            <tr><td>Author (optional):</td><td>${h.text('author')}</td></tr>
            <tr><td>Website (optional):</td><td>${h.text('author_website')}</td></tr>
            </table>
            <table>
            <tr><td style="width:75%;">${h.textarea('body', rows=8)}</td>
            <td style="width:25%; opacity:0.5; padding:10px;">No HTML codes allowed. URL's will automatically be converted to links.</td></tr>
            </table>
            ${h.hidden('post_id', value=post.id)}
            ${h.hidden('antiSpam', id='antiSpam', value='Please do not alter')}
            <p>${h.submit('comment_submit', 'Submit', disabled='true')}</p>
            ${h.end_form()}<br>
        </div>
        <div class="comments">
            <h2>Comments</h2>
            <div id="comments_holder">
            <!--
                Comments inserted here via javascript and ajax  
            -->
            </div>
            <div id="ajax_loading">
                <img src="/img/ajax-loader.gif">
            </div>
        </div>
        <%
            context.write('<div class="comment_post_identifier">')
            context.write(h.url(controller='comment', action='get_all', id=post.id))
            context.write('</div>')
        %>
    </div>
</%def>
