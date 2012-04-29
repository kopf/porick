# -*- coding: utf-8 -*-
<%! from webhelpers.html import literal %>
<!DOCTYPE html>
<html lang="en">
    <head>
        ${self.head()}
    </head>
    <body>
        ${self.body_header()}
        ${self.body_content()}
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
    <link rel="stylesheet" type="text/css" href="/bootstrap/css/bootstrap.css" />
</%def>

<%def name="head_js()">
</%def>

<%def name="body_js()">
    <script type="text/javascript" src="/js/jquery-1.7.2.js"></script>
    <script type="text/javascript" src="/bootstrap/js/bootstrap.js"></script>
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

<%def name="body_header()">
    <div class="navbar navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container">
                <a class="brand" href="#">Porick</a>
                <div class="nav-collapse">
                    <ul class="nav">
                        <li class="active"><a href="/">Home</a></li>
                    </ul>
                    <ul class="nav pull-right">
                        <form class="navbar-search pull-left" action="">
                            <input type="text" class="search-query span2" placeholder="Search">
                        </form>
                        <li class="divider-vertical"></li>
                        <li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">Account <b class="caret"></b></a>
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
