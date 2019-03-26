<%doc>
Created in 2019-02-20 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/20 (Simon) - Initial template
2019/03/26 (Simon) - Changed page arguments, updated UI
</%doc>


<%doc>
Mako variables:
    (string) title
    (string) message
    (string) linkaddr
    (string) linktext
</%doc>


<%page args="user=None, title=None, message=None, linkaddr=None, linktext=None"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user"/>
        </header>
        <section class="ui container">
            <div class="dialog">
                % if title is not None:
                <h1>${title}</h1>
                % endif
                % if message is not None:
                <p>${message}</p>
                % endif
                % if (linkaddr is not None) or (linktext is not None):
                <a href="${linkaddr}">${linktext}</a>
                % endif
            </div>
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>