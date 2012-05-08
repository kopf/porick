<%inherit file="/base.mako"/>

<%def name="body_content()">
    <form class="well create_new_quote" action="${h.url(controller='account', action='login')}" method="post">
        <label class="control-label" for="username">Username:</label>
        <div class="controls">
            <input type="text" class="input-xlarge" id="username" name="username">
        </div>

        <label class="control-label" for="password">Password:</label>
        <div class="controls">
            <input type="password" class="input-xlarge" id="password" name="password">
        </div>

        <div>
            <button type="submit" class="btn btn-primary">Sign up!</button>
        </div>
    </form>
</%def>

