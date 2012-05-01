<%inherit file="base.mako"/>

<%def name="body_content()">
    % for quote in c.quotes:
        <div class="well quote">
            <ul class="metadata">
                <li><a href="${h.url(controller='browse', action='view_one', ref_id=quote.id)}">${quote.submitted}</a></li>
                <li>Up ${quote.rating}</li>
                <li>Down ${quote.votes - quote.rating}</li>
                <li class="date_submitted nomargin">${quote.submitted}</li>
            </ul>
            ${self.insert_quote_body(quote)}
        </div>
    % endfor
</%def>

<%def name="insert_quote_body(quote)">
<pre class="content">${quote.body.decode('latin1') | h}</pre>
</%def>

