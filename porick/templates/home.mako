<%inherit file="base.mako"/>
<%namespace file="helpers.mako" import="display_hero_unit"/>

<%def name="body_content()">
    ${display_hero_unit('Porick.',
                        '''Porick is yet another IRC Quotes web application, designed to replace <i>Chirpy!</i>''',
                        'Start browsing', 
                        h.url(controller='browse', action='main'))}
</%def>

<%def name="side_text()">
</%def>
