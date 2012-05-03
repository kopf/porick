<%inherit file="base.mako"/>

<%def name="body_content()">
    % for quote in c.quotes:
        <div class="well quote">
            <div class="votes">
                <div class="vote up"><i class="icon-circle-arrow-up"> </i></div>
                <div class="score">${quote.rating}</div>
                <div class="vote down"><i class="icon-circle-arrow-down"> </i></div>
            </div>
            <ul class="metadata">
                <li><a href="${h.url(controller='browse', action='view_one', ref_id=quote.id)}">${quote.submitted}</a></li>
                <li>Score ${quote.rating}</li>
                <li>Up ${quote.votes}</li>
                <li>Down ${quote.votes - quote.rating}</li>
                <li class="date_submitted nomargin">${quote.submitted}</li>
            </ul>
            ${self.insert_quote_body(quote)}
        </div>
    % endfor
</%def>

<%def name="insert_quote_body(quote)">
<pre class="content">${quote.body | h}</pre>
</%def>

