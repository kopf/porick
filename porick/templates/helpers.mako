<%def name="display_hero_unit(heading, subheading, linktext, url)">
    <div class="hero-unit">
        <h1>${heading}</h1>
        <p>${h.literal(subheading)}</p>
        % if linktext:
            <p>
                <a class="btn btn-primary btn-large" href="${url}">
                    ${linktext}
                </a>
            </p>
        % endif
    </div>
</%def>
