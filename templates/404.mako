<%doc>
Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/23 (Simon) - added initial landing site
2019/04/01 (Simon) - changed to Mako template
2019/04/24 (Simon) - Updated template
2019/05/15 (Simon) - Removed HTML comments, replaced with <%doc> tags
                   - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
</%doc>


<%page args="user=None"/>
<%inherit file="_base.mako"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <title>PSYSC - 404</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='index'"/>
        </header>
        <div class="ui container">
            <div class="ui message">
                <h1 class="ui red header">
                    404
                    <div class="sub header">Page not found.</div>
                </h1>
            </div>
        </div>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>