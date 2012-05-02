<%inherit file="/base.mako"/>

<%def name="body_content()">
    <div class="hero-unit">
        <h1>Success!</h1>
        <p>Awwwww ye! That quote will be up in no time, once it's approved.</p>
        <p>
            <a class="btn btn-primary btn-large" href="${h.url(controller='browse', action='main')}">
                Continue Browsing
            </a>
        </p>
    </div>
</%def>
