<%inherit file="/base.mako"/>
<%namespace file="/helpers.mako" import="display_hero_unit"/>

<%def name="head_title()">Welcome!</%def>

<%def name="body_content()">
    ${display_hero_unit('Welcome!', 
                        '''Your registration is now complete. Now you can begin voting on quotes and submitting your own.''',
                        '''Let's go!''', 
                        h.url(controller='browse', action='main'))}
</%def>

