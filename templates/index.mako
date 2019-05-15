<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/08 (Simon) - added initial landing site
2019/02/13 (Simon) - Added Mako templating
2019/02/14 (Simon) - renamed to index.mako
2019/02/15 (Simon) - added <section> tags
2019/03/26 (Simon) - Changed page arguments
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
                   - Replaced placeholder text
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
        <title>PSYSC - Home</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='index'"/>
        </header>
        <section class="ui container">
            <p>The Philippine Society of Youth Science Clubs (PSYSC) is the premier non-profit organization that promotes the public understanding of Science, Technology, and the Environment in the country. For 48 years, PSYSC has been upholding its values and thrust by conducting various activities that encourage the youth to participate in the science clubbing movement, enabling them to take action in the fields of science and technology in pursuit of national progress.</p>
        </section>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>