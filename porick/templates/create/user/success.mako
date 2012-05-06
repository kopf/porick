<%inherit file="/base.mako"/>

<%def name="body_content()">
    ${self.display_hero_unit('Welcome!', 
                             '''Your registration is now complete. Now you can begin voting on quotes and submitting
                             your own.''',
                             '''Let's go!''', 
                             h.url(controller='browse', action='main'))}
</%def>

