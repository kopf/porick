<%inherit file="base.mako"/>

<%def name="head_title()">${c.message}</%def>

<%def name="custom_css()">
    <link rel="stylesheet" type="text/css" href="/css/error.css" />
</%def>

<%def name="body_content()">
    <div class="hero-unit">
        <h1>${c.message}</h1>
    </div>
</%def>

<%def name="side_text()">
    oh shit
</%def>
