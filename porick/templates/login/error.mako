<%inherit file="form.mako"/>

<%def name="body_content()">
    <div class="alert alert-error">
        ${c.error}
    </div>
    ${parent.body_content()}
</%def>
