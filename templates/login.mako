<%doc>
Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/23 (Simon) - added initial login template
</%doc>


<%page args="user=None"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body style="min-width:320px; margin:0px; padding:0px">
        <header>
            <%include file="header.mako" args="user=user, current='view'"/>
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