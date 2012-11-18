<%inherit file="/base.mako"/>

<%def name="head_title()">Set Password</%def>

<%def name="body_content()">
    <form class="well create_new_quote" action="${h.url(controller='account', action='reset_password', key=c.key)}" method="post">
        <label class="control-label" for="password">Password:</label>
        <div class="controls">
            <input type="password" class="input-xlarge" id="password" name="password">
        </div>

        <label class="control-label" for="password_confirm">Password (confirm):</label>
        <div class="controls">
            <input type="password" class="input-xlarge" id="password_confirm" name="password_confirm">
        </div>
        <div>
            <button type="submit" class="btn btn-primary">Set Password</button>
        </div>
    </form>
</%def>

