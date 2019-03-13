<%doc>
Created in 2019-03-12 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/12 (Simon) - Intial template code
2019/03/13 (Simon) - Updated displayed columns
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="data=None, q=''"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/approve.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">Pending Applications</h1>
            <hr>
            % if (data is not None) and (len(data) > 0):
            <form method="get" action="" id="filter-form">
                <input type="text" name="q" value="${q}"/><button type="submit">search</button>
            </form>
            <table>
                <tr>
                    <th></th>
                    <th></th>
                    <th>application ID</th>
                    <th>club name</th>
                    <th>school</th>
                    <th>adviser/s</th>
                    <th>payment amount</th>
                    <th>payment date</th>
                    <th>contact</th>
                    <th>email</th>
                    <th>last updated</th>
                </tr>
                % for app in data:
                <tr>
                    <td><a href="view/${app['appID']}">view</a></td>
                    <td><a href="approve/${app['appID']}">approve</a>/<a href="reject/${app['appID']}">reject</a></td>
                    <td>${app['appID']}</td>
                    <td>${app['clubName']}</td>
                    <td>${app['school']}</td>
                    <td>${app['adviserName']}</td>
                    <td>${app['paymentAmount']}</td>
                    <td>${app['paymentDate']}</td>
                    <td>${app['contact']}</td>
                    <td><a href="mailto:${app['email']}">${app['email']}</a></td>
                    <td>${app['dateCreated']}</td>
                </tr>
                % endfor
            </table>
            % else:
            <p class="center">Database is empty</p>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>