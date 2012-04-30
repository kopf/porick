<%inherit file="base.mako"/>

<%def name="body_content()">
    % for quote in c.quotes:
        <div class="well">
            ${self.insert_quote_body(quote)}
        </div>
    % endfor
</%def>

<%def name="insert_quote_body(quote)">
<pre class="quote_body">${quote.body}</pre>
</%def>

