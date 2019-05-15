<%doc>
Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/23 (Simon) - added initial login template
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
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
        <title>PSYSC - Login</title>
    </head>
    <body style="min-width:320px; margin:0px; padding:0px">
        <header>
            <%include file="_header.mako" args="user=user, current='view'"/>
        </header>
        <div class="ui middle aligned center aligned grid">
            <div class="column" style="max-width:450px">
                <h2 class="ui blue image header">Log in to PSYSC</h2>
                <form class="ui large form" method="POST" action="verify">
                    <div class="ui raised blue segment">
                        <div class="field">
                            <div class="ui left icon input">
                                <i class="user icon"></i>
                                <input type="text" name="ID" placeholder="User ID">
                            </div>
                        </div>
                        <div class="field">
                            <div class="ui left icon input">
                                <i class="lock icon"></i>
                                <input type="password" name="PIN" placeholder="PIN Code">
                            </div>
                        </div>
                        <button class="ui fluid large blue submit button" type="submit">Login</button>
                  </div>
                  <div class="ui error message"></div>
                </form>
            </div>
        </div>
    </body>
</html>