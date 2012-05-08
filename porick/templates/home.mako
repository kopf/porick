<%inherit file="base.mako"/>
<%namespace file="helpers.mako" import="display_hero_unit"/>

<%def name="body_content()">
    ${display_hero_unit(h.literal(c.site_name),
                        h.literal(c.welcome_text),
                        h.literal(c.button_text), 
                        h.url(controller='browse', action='main'))}
</%def>

<%def name="side_text()">
</%def>
