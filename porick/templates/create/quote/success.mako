<%inherit file="/base.mako"/>

<%def name="body_content()">
    ${self.display_hero_unit('Success!', 
                             '''Awwwww ye! That quote will be up in no time, once it's approved.''',
                             'Continue Browsing', 
                             h.url(controller='browse', action='main'))}
</%def>

