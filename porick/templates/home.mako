<%inherit file="base.mako"/>

<%def name="body_content()">
    <div class="hero-unit">
        <h1>${h.literal(c.site_name)}</h1>
        <p>${h.literal(c.welcome_text)}</p>
        <p>
            <a class="btn btn-primary btn-large" href="${h.url(controller='browse', action='main')}">
                ${c.button_text}
            </a>
        </p>
    </div>
</%def>

<%def name="side_text()">
</%def>
