<%inherit file="base.mako"/>

<%def name="body_content()">
    % for quote in c.quotes:
        <div class="well quote">
            <div class="votes">
                <div class="vote up" title="${quote.votes} upvotes"><i class="icon-circle-arrow-up"> </i></div>
                <div class="score">${quote.rating}</div>
                <div class="vote down" title="${quote.votes - quote.rating} downvotes"><i class="icon-circle-arrow-down"> </i></div>
            </div>
            <ul class="metadata">
                <li><a href="${h.url(controller='browse', action='view_one', ref_id=quote.id)}">${quote.submitted}</a></li>
                <li class="top_right nomargin"></li>
            </ul>
            ${self.insert_quote_body(quote)}
        </div>
    % endfor
</%def>

<%def name="insert_quote_body(quote)">
<div class="content">
    <pre>${quote.body | h}</pre>
    % if quote.notes:
        <hr>
        <div class="extra_info notes">
            <h6>Notes:</h6>
            <span class="details">
                ${quote.notes}
            </span>
        </div>
    % endif
</div>
% if quote.id in c.tags:
    <div class="extra_info tags">
        % for tag in c.tags[quote.id]:
            <a href="${h.url(controller='browse', action='tags', tag=tag)}">
                <span class="label label-important">
                    ${tag}
                </span>
            </a>
        % endfor
    </div>
% endif
</%def>

