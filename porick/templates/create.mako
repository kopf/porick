<%inherit file="base.mako"/>

<%def name="body_content()">
    <form class="well create_new_quote">
        <label>Quote text</label>
        <textarea class="input-xlarge" id="quote_body" rows=10 cols=80></textarea>
        <label>Additional information, if any:</label>
        <textarea class="input-xlarge" id="extra_info" rows=5 cols=80></textarea>
        <input type="text" class="input-xlarge" id="tags" placeholder="Enter some tags here...">
        <div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>
    </form>
</%def>
