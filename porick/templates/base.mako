# -*- coding: utf-8 -*-
<%! from webhelpers.html import literal %>
<!DOCTYPE html>
<html lang="en">
    <head>
        ${self.head()}
    </head>
    <body>
        ${self.body_header()}
        <div class="container">
            <div class="side_text">
                ${self.side_text()}
            </div>
            % if c.messages:
                % for message in c.messages:
                    <div class="alert alert-${message.get('level', 'error')}">
                        ${message.get('msg', '')}
                    </div>
                % endfor
            % endif
            ${self.body_content()}
            ${self.body_footer()}
        </div>
        ${self.body_js()}
    </body>
</html>

<%def name="head()">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="icon" type="image/png" href="/img/favicon.png">
    ${self.head_extra_metadata()}
    <title>${self.head_title_tag()}</title>
    ${self.head_css()}
    ${self.head_js()}
    <link rel="icon" type="image/png" href="/img/favicon.ico" />
</%def>

<%def name="head_extra_metadata()">
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

<%def name="side_text(capitalize=False)">
    % if c.page == 'tags' and 'tag_filter' in c.__dict__:
        % if capitalize:
            Tag: 
        % else:
            tag: 
        % endif
        ${c.tag_filter}
    % else:
        % if capitalize:
            ${c.page.capitalize()}
        % else:
            ${c.page}
        % endif
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
                        <li class="${'active' if c.page == 'deleted' else ''}"><a href="${h.url(controller='browse', action='deleted')}">Deleted</a></li>
                        <li class="${'active' if c.page == 'tags' else ''}"><a href="${h.url(controller='browse', action='tags')}">Tags</a></li>
                    </ul>
                    <a class="btn btn-small btn-success" href="${h.url(controller='create', action='quote')}">Submit</a>
                    <ul class="nav pull-right">
                        <form class="navbar-search pull-left" action="${h.url(controller='browse', action='search')}" method="post">
                            <input type="text" class="search-query span2" placeholder="Search" name="keyword">
                        </form>
                        <li class="divider-vertical"></li>
                        ${self.account_dropdown()}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="account_dropdown()">
    % if c.logged_in and not c.page == 'logout':
        <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">${c.user.username} <b class="caret"></b></a>
            <ul class="dropdown-menu">
                % if h.is_admin():
                    <li class="nav-header">Admin</li>
                    <li><a href="${h.url(controller='browse', action='unapproved')}">Unapproved Quotes</a></li>
                    <li><a href="${h.url(controller='browse', action='reported')}">Reported Quotes</a></li>
                    <li><a href="${h.url(controller='browse', action='disapproved')}">Disapproved Quotes</a></li>
                    <li class="divider"></li>
                % endif
                <li><a href="${h.url(controller='browse', action='favourites')}">My Favourites</a></li>
                <li class="divider"></li>
                <li><a href="${h.url(controller='account', action='logout')}">Log out</a></li>
            </ul>
        </li>
    % else:
        <li><a href="${h.url(controller='account', action='create')}">Sign up</a></li>
        <li><a href="${h.url(controller='account', action='login', redirect_url=h.url.current())}">Log in</a></li>
    % endif
</%def>

<%def name="body_content()">
</%def>

<%def name="body_footer()">
</%def>

