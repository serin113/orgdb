<%doc>
Created in 2019-03-15 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/15 (Simon) - Initial template
</%doc>


<%doc>
Mako variables:
    (list) data
</%doc>


<%page args="data=None"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/index.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            % if data is not None:
            ${data}
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>