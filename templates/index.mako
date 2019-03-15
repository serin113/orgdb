<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/08 (Simon) - added initial landing site
2019/02/13 (Simon) - Added Mako templating
2019/02/14 (Simon) - renamed to index.mako
2019/02/15 (Simon) - added <section> tags
</%doc>


<%doc>
Mako variables:
    none
</%doc>


<html>
    <head>
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="semantic/dist/semantic.min.css">
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
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod quam sit amet urna convallis, eget scelerisque risus hendrerit. Quisque interdum dapibus justo a faucibus. Proin eu dui ac augue blandit fringilla a nec metus. Nullam ut nunc ut ex mollis placerat. Integer at sapien enim. Proin pulvinar justo quis erat tempus, sit amet gravida tortor volutpat. Curabitur imperdiet justo quis orci interdum, sit amet efficitur sapien vestibulum. Duis lobortis ornare purus, eget fermentum erat. Vestibulum viverra, metus non consequat imperdiet, magna ex tristique magna, quis hendrerit elit lectus sollicitudin lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non gravida nibh, quis condimentum odio.</p>
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>