<%inherit file="browse.mako"/>

<%def name="custom_js()">
    <script type="text/javascript" src="/js/voting.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            setupVoteClickHandlers();
        });
    </script>
</%def>

<%def name="custom_css()">
    <style type="text/css">
        .vote { cursor: pointer; }
    </style>
</%def>

