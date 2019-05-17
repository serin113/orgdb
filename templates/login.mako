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
2019/05/17 (Simon) - UI updated
                   - Uses login.css for styling
                   - Removed unused parameter
</%doc>


<%inherit file="_base.mako"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/login.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <title>PSYSC - Login</title>
    </head>
    <body>
        <div class="ui middle aligned center aligned grid" id="login_form">
            <div class="column">
                <div class="ui left aligned container">
                    <a href="/" class="ui small basic blue icon button" id="button"><i class="home icon"></i></a>
                </div>
                <h1 class="ui left aligned image header">
                    <img src="/static/psysc.png" class="ui image" id="#logo">
                    <div class="content">
                        <a href="/">PSYSC</a>
                        <div class="tiny sub header">Affiliation Database</div>
                    </div>
                </h1>
                <form class="ui large form" method="POST" action="verify">
                    <div class="ui stacked blue segment">
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