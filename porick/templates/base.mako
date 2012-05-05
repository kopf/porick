# -*- coding: utf-8 -*-
<%! from webhelpers.html import literal %>
<!DOCTYPE html>
<html lang="en">
    <head>
        ${self.head()}
    </head>
    <body>
        ${self.body_header()}
        <div class="side_text">
            ${self.side_text()}
        </div>
        <div class="container">
            ${self.body_content()}
            ${self.body_footer()}
        </div>
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
    <link rel="stylesheet" type="text/css" href="/css/base.css" />
    <link rel="stylesheet" type="text/css" href="/bootstrap/css/bootstrap.css" />
    ${self.custom_css()}
</%def>

<%def name="custom_css()">
</%def>

<%def name="head_js()">
</%def>

<%def name="body_js()">
    <script type="text/javascript" src="/js/jquery/jquery-1.7.2.js"></script>
    <script type="text/javascript" src="/bootstrap/js/bootstrap.js"></script>
    ${self.custom_js()}
</%def>

<%def name="custom_js()">
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

<%def name="side_text()">
    % if c.page == 'tags' and c.tag_filter:
        tag: ${c.tag_filter}
    % else:
        ${c.page}
    % endif
</%def>

<%def name="body_header()">
    <div class="navbar navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container">
                <a class="brand" href="/">Porick</a>
                <div class="nav-collapse">
                    <ul class="nav">
                        <li class="${'active' if c.page == 'browse' else ''}"><a href="${h.url(controller='browse', action='main')}">Browse</a></li>
                        <li class="${'active' if c.page == 'best' else ''}"><a href="${h.url(controller='browse', action='best')}">Best</a></li>
                        <li class="${'active' if c.page == 'worst' else ''}"><a href="${h.url(controller='browse', action='worst')}">Worst</a></li>
                        <li class="${'active' if c.page == 'random' else ''}"><a href="${h.url(controller='browse', action='random')}">Random</a></li>
                        <li class="${'active' if c.page == 'tags' else ''}"><a href="${h.url(controller='browse', action='tags')}">Tags</a></li>
                    </ul>
                    <a class="btn btn-small btn-success" href="${h.url(controller='create', action='main')}">Submit</a>
                    <ul class="nav pull-right">
                        <form class="navbar-search pull-left" action="">
                            <input type="text" class="search-query span2" placeholder="Search">
                        </form>
                        <li class="divider-vertical"></li>
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">Sign in <b class="caret"></b></a>
                            <ul class="dropdown-menu">
                                <li><a href="#">Action</a></li>
                                <li><a href="#">Another action</a></li>
                                <li><a href="#">Something else here</a></li>
                                <li class="divider"></li>
                                <li><a href="#">Separated link</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="body_content()">
</%def>

<%def name="body_footer()">
</%def>
