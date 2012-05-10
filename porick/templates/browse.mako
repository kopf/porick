<%inherit file="base.mako"/>

<%def name="head_title()">
    % if not c.page == 'tags':
        ${c.page.capitalize()} Quotes
    % else:
        Browse Quotes
    % endif
</%def>

<%def name="body_content()">
    % if not (c.paginator or c.quote):
        <div class="hero-unit">
            <h1>No quotes found.</h1>
            <p>Get your users to add some!</p>
        </div>
    % else:
        % if c.quote:
            ${self.display_quote(c.quote)}
        % else:
            ${self.display_pagination()}
            % for quote in c.paginator:
                ${self.display_quote(quote)}
            % endfor
            ${self.display_pagination()}
        % endif
    % endif
</%def>

<%def name="display_quote(quote)">
    <div class="well quote">
        ${self.insert_vote_buttons(quote)}
        <ul class="metadata">
            <li><a href="${h.url(controller='browse', action='view_one', ref_id=quote.id)}">${quote.submitted}</a></li>
            <li class="top_right nomargin"></li>
        </ul>
        ${self.insert_quote_body(quote)}
    </div>
</%def>

<%def name="insert_vote_buttons(quote)">
    <div class="votes">
        <div class="vote up" title="${h.get_score_mouseover(quote, 'up')}" data-quote_id="${quote.id}">
            :
        </div>
        <div class="score">${quote.rating}</div>
        <div class="vote down" title="${h.get_score_mouseover(quote, 'down')}" data-quote_id="${quote.id}">
            ;
        </div>
    </div>
</%def>

<%def name="insert_quote_body(quote)">
    <div class="content">
        <pre>${quote.body | h}</pre>
        % if quote.notes:
            <hr>
            <h6>${quote.notes}</h6>
        % endif
    </div>
    % if quote.tags:
        <div class="extra_info tags">
            % for tag in quote.tags:
                <a href="${h.url(controller='browse', action='tags', tag=tag.tag)}">
                    <span class="label label-important">
                        ${tag.tag}
                    </span>
                </a>
            % endfor
        </div>
    % endif
</%def>

<%def name="display_pagination()">
    <div class="pagination">
        ${c.paginator.pager(curpage_attr={'class': 'bootstrap_style'},
                            dotdot_attr={'class': 'bootstrap_style'},
                            symbol_previous='&#171;',
                            symbol_next='&#187;')}
    </div>
</%def>
