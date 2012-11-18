<%inherit file="/base.mako"/>

<%def name="head_title()">Log in</%def>

<%def name="body_content()">
    <form class="well create_new_quote" action="${h.url(controller='account', action='login', redirect_url=c.redirect_url)}" method="post">
        <label class="control-label" for="username">Username:</label>
        <div class="controls">
            <input type="text" class="input-xlarge" id="username" name="username">
        </div>

        <label class="control-label" for="password">Password:</label>
        <div class="controls">
            <input type="password" class="input-xlarge" id="password" name="password">
        </div>

        <div>
            <button type="submit" class="btn btn-primary">Sign in</button>
        </div>
        <div style="margin-top:1em;"><a href="${h.url(controller='account', action='reset_password')}">Forgot your password?</a></div>
    </form>
</%def>

