<%inherit file="browse.mako"/>

<%def name="custom_js()">
    <script type="text/javascript" src="/js/voting.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            setupVoteClickHandlers();
        });
    </script>
</%def>

<%def name="custom_css()">
    <style type="text/css">
        .vote { cursor: pointer; }
    </style>
</%def>

<%def name="insert_vote_buttons(quote)">
    <% voted = h.check_if_voted(quote) %>
    <div class="votes">
        <div class="vote up ${'voted' if voted == 'up' else ''}" title="${h.get_score_mouseover(quote, 'up')}" data-quote_id="${quote.id}">
            :
        </div>
        <div class="score">${quote.rating}</div>
        <div class="vote down ${'voted' if voted == 'down' else ''}" title="${h.get_score_mouseover(quote, 'down')}" data-quote_id="${quote.id}">
            ;
        </div>
    </div>
</%def>
