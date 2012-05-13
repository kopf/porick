<%inherit file="browse.mako"/>

<%def name="custom_js()">
    % if h.show_approval_buttons():
        <script type="text/javascript" src="/js/approval.js"></script>
    % endif
    <script type="text/javascript" src="/js/voting.js"></script>
    <script type="text/javascript" src="/js/favourites.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            setupVoteClickHandlers();
            setupFavouritesClickHandlers();
            % if h.show_approval_buttons():
                setupApproveClickHandlers();
            % endif
        });
    </script>
</%def>

<%def name="insert_vote_buttons(quote)">
    <% voted = h.check_if_voted(quote) %>
    <div class="votes">
        <div class="vote up logged_in ${'voted' if voted == 'up' else ''}" title="${h.get_score_mouseover(quote, 'up')}" data-quote_id="${quote.id}">
            :
        </div>
        <div class="score">${quote.rating}</div>
        <div class="vote down logged_in ${'voted' if voted == 'down' else ''}" title="${h.get_score_mouseover(quote, 'down')}" data-quote_id="${quote.id}">
            ;
        </div>
    </div>
</%def>

<%def name="insert_favourite_button(quote)">
    % if quote in c.user.favourites:
        <span class="favourite logged_in favourited" data-quote_id="${quote.id}">N</span>
    % else:
        <span class="favourite logged_in" data-quote_id="${quote.id}">O</span>
    % endif
</%def>