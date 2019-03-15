<%doc>
Created in 2019-02-20 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/20 (Simon) - Initial template
</%doc>


<%doc>
Mako variables:
    (string) title
    (string) message
    (string) linkaddr
    (string) linktext
</%doc>


<%page args="title=None, message=None, linkaddr=None, linktext=None"/>


<html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
        <script
          src="https://code.jquery.com/jquery-3.1.1.min.js"
          integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
          crossorigin="anonymous"></script>
        <script src="semantic/dist/semantic.min.js"></script>

    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
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