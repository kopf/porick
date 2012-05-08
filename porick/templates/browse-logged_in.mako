<%inherit file="browse.mako"/>

<%def name="custom_js()">
    <script type="text/javascript" src="/js/voting.js"></script>
</%def>

<%def name="custom_css()">
    <style type="text/css">
        .vote { cursor: pointer; }
    </style>
</%def>

<%def name="extra_body_parameters()">onload="setupVoteClickHandlers();"</%def>
