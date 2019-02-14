<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/08 - added initial landing site
2019/02/13 - Added Mako templating
2019/02/14 - renamed to index.mako
</%doc>


<%doc>
Mako variables:
    none
</%doc>


<html>
    <head>
        <link rel="stylesheet" href="/styles/index.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <a href="/add">Add Record</a><br>
        <a href="/view">View Record</a>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>