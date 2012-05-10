<%inherit file="/base.mako"/>
<%namespace file="/helpers.mako" import="display_hero_unit"/>

<%def name="head_title()">Quote added</%def>

<%def name="body_content()">
    ${display_hero_unit('Success!', 
                        '''Awwwww ye! That quote will be up in no time, once it's approved.''',
                        'Continue Browsing', 
                        h.url(controller='browse', action='main'))}
</%def>

