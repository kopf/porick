<%inherit file="base.mako"/>

<%def name="head_title()">Tag cloud</%def>

<%def name="body_content()">
    <div class="tags cloud">
        % for tag in c.tags:
            <a href="${h.url(controller='browse', action='tags', tag=tag)}">
                <span class="label ${h.random.choice(c.rainbow) if c.rainbow else 'label-important'}" style="font-size:${c.tags[tag] + 10}px;">
                    ${tag}
                </span>
            </a>
        % endfor
    </div>
</%def>
