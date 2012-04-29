# -*- coding: utf-8 -*-
<%! from webhelpers.html import literal %>
<!DOCTYPE html>
<html lang="en">
    <head>
        ${self.head()}
    </head>
    <body>
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span2">
                    ${self.sidebar_content()}
                </div>
                <div class="span10">
                    ${self.body_content()}
                </div>
            </div>
        </div>
        ${self.body_footer()}
        ${self.body_js()}
    </body>
</html>

<%def name="head()">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>${self.head_title_tag()}</title>
    ${self.head_css()}
    ${self.head_js()}
    <link rel="icon" type="image/png" href="/img/favicon.ico" />
</%def>

<%def name="head_css()">
    <link rel="stylesheet" type="text/css" href="/bootstrap/bootstrap.css" />
</%def>

<%def name="head_js()">
</%def>

<%def name="body_js()">
</%def>
## Title of this page to be used in the header <title>.
<%def name="head_title_tag()"><%
    from mako.runtime import capture
    from webhelpers.html import literal
    t = h.cgi_unescape(capture(context, self.head_title))
    if t == 'Porick' in t:
        return t
    else:
        return _('{title} - Porick').format(title=t)
%></%def>
## You should usually overwrite this one and " - Porick" will get appended
<%def name="head_title()">Porick</%def>

<%def name="sidebar_content()">
</%def>

<%def name="body_content()">
</%def>

<%def name="body_footer()">
</%def>
