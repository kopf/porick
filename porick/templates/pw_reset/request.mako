<%inherit file="/base.mako"/>

<%def name="head_title()">Reset Password</%def>

<%def name="body_content()">
    <form class="well create_new_quote" action="${h.url(controller='account', action='reset_password', redirect_url=c.redirect_url)}" method="post">
        <label class="control-label" for="email">Email address:</label>
        <div class="controls">
            <input type="text" class="input-xlarge" id="email" name="email">
        </div>
        <div>
            <button type="submit" class="btn btn-primary">Reset Password</button>
        </div>
    </form>
</%def>

