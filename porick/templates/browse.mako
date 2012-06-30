<%inherit file="base.mako"/>

<%def name="custom_js()">
    % if c.logged_in:
        % if h.show_approval_button():
            <script type="text/javascript" src="/js/approval.js"></script>
        % endif
        <script type="text/javascript" src="/js/voting.js"></script>
        <script type="text/javascript" src="/js/favourites.js"></script>
        <script type="text/javascript" src="/js/reporting.js"></script>
        <script type="text/javascript" src="/js/delete.js"></script>
        <script type="text/javascript">
            $(document).ready(function() {
                setupVoteClickHandlers();
                setupFavouritesClickHandlers();
                setupReportingClickHandlers();
                % if c.page == 'unapproved':
                    setupDisapproveClickHandlers();
                % else:
                    setupDeleteClickHandlers();
                % endif
                
                % if h.show_approval_button():
                    setupApproveClickHandlers();
                % endif
            });
        </script>
    % endif
</%def>

<%def name="head_title()">
    % if 'search' in c.page or c.page == 'tags':
        ${self.side_text(capitalize=True)}
    % else:
        ${c.page.capitalize()} Quotes
    % endif
</%def>

<%def name="body_content()">
    % if not (c.paginator or c.quote):
        <div class="hero-unit">
            <h1>No quotes found.</h1>
            <p>
            % if c.page == 'favourites':
                Just click the little heart in the top-right hand corner of any quote and it'll be added to your
                favourites!
            % elif c.page == 'unapproved': 
                Best go grab a can.
            % elif c.page in ['reported', 'deleted', 'disapproved']: 

            % else: 
                Get your users to add some!
            % endif
            </p>
        </div>
    % else:
        % if c.quote:
            ${self.display_quote(c.quote)}
        % else:
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
            <li>
                <a href="${h.url(controller='browse', action='view_one', ref_id=quote.id)}" class="date">${quote.submitted.strftime("%d. %B %Y @ %H:%M")}</a>
                % if quote.submitted_by:
                    <span class="submitted_by">
                        by ${quote.submitted_by.username}
                    </span>
                % endif
            </li>
            <li class="top_right nomargin">
                <ul class="top_right_controls">
                    <li><div class="quote_control report ${'logged_in' if c.logged_in else ''}" title="Report" ${self.data_quote_id(quote)}>W</div></li>
                    <li><div>${self.insert_favourite_button(quote)}</div></li>
                    % if h.show_approval_button():
                        <li><div class="quote_control logged_in approve" title="Approve" ${self.data_quote_id(quote)}>/</div></li>
                    % endif
                    % if h.quote_is_deleteable(quote):
                        <li><div class="quote_control logged_in delete" title="${'Disapprove' if c.page == 'unapproved' else 'Delete'}" ${self.data_quote_id(quote)}>×</div></li>
                    % endif
                </ul>
            </li>
        </ul>
        ${self.insert_quote_body(quote)}
        <div class="bottom_metadata">
            ${self.insert_quote_tags(quote)}
        </div>
    </div>
</%def>

<%def name="insert_vote_buttons(quote)">
    <% voted = h.check_if_voted(quote) %>
    <div class="votes">
        <div class="quote_control vote up ${'logged_in' if c.logged_in else ''} ${'voted' if voted == 'up' else ''}" title="${h.get_score_mouseover(quote, 'up')}" ${self.data_quote_id(quote)}>
            :
        </div>
        <div class="score">${quote.rating}</div>
        <div class="quote_control vote down ${'logged_in' if c.logged_in else ''} ${'voted' if voted == 'down' else ''}" title="${h.get_score_mouseover(quote, 'down')}" ${self.data_quote_id(quote)}>
            ;
        </div>
    </div>
</%def>

<%def name="insert_favourite_button(quote)">
    % if not c.logged_in:
        <span class="quote_control favourite" title="Favourite">O</span>
    % elif quote in c.user.favourites:
        <span class="quote_control favourite logged_in favourited" title="Favourite" ${self.data_quote_id(quote)}>N</span>
    % else:
        <span class="quote_control favourite logged_in" title="Favourite" ${self.data_quote_id(quote)}>O</span>
    % endif
</%def>

<%def name="insert_quote_body(quote)">
    <div class="content">
        <pre>${quote.body | h}</pre>
        % if quote.notes:
            <hr>
            <h6>${quote.notes}</h6>
        % endif
    </div>
</%def>

<%def name="insert_quote_tags(quote)">
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
    % if c.paginator.page_count > 1:
        <div class="paginator_container">
            <div class="pagination">
                ${c.paginator.pager(curpage_attr={'class': 'bootstrap_style'},
                                    dotdot_attr={'class': 'bootstrap_style'},
                                    symbol_previous='&#171;',
                                    symbol_next='&#187;')}
            </div>
        </div>
    % endif
</%def>

<%def name="data_quote_id(quote)">data-quote_id="${quote.id}"</%def>
