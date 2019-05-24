<%doc>
Created in 2019-02-20 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/20 (Simon) - Initial template
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
2019/04/02 (Simon) - Updated layout, moved some inline scripts to dialog.js
2019/04/24 (Simon) - Added option for additional button
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header.mako > _header.mako, footer.mako > _footer.mako
                   - Renamed dialog.js > back.js
2019/05/18 (Simon) - Added spacing between title+message and links
2019/05/24 (Simon) - Add "header" boolean arg
</%doc>


<%doc>
Mako variables:
    (string) title
    (string) message
    (string) linkaddr
    (list) errors
        (tuple) error
            (<message>, <field>, <value>)
    (string) linktext
</%doc>


<%page args="user=None, title=None, message=None, errors=None, linkaddr=None, linktext=None, linkaddr2=None, linktext2=None, header=True"/>
<%inherit file="_base.mako"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/back.js"></script>
        <title>PSYSC</title>
    </head>
    <body>
        % if header:
        <header>
            <%include file="_header.mako" args="user=user"/>
        </header>
        % endif
        <section class="ui container">
            <div class="ui message">
                % if title is not None:
                <h1 class="header">${title}</h1>
                % endif
                % if message is not None:
                <p>${message}</p>
                % endif
                % if errors is not None:
                <div class="ui list">
                    % for e in errors:
                    <div class="item">
                        <b>[${str(e[0])}]</b> '${str(e[1])}': ${str(e[2])}
                    </div>
                    % endfor
                </div>
                % endif
                % if (linkaddr is not None) or (linktext is not None):
                <div class="ui hidden divider"></div>
                <a href="${linkaddr}" class="ui small basic blue button" id="button">${linktext}</a>
                % endif
                % if (linkaddr2 is not None) or (linktext2 is not None):
                <a href="${linkaddr2}" class="ui small basic blue button" id="button2">${linktext2}</a>
                % endif
            </div>
        </section>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>