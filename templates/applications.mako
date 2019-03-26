<%doc>
Created in 2019-03-12 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/12 (Simon) - Intial template code
2019/03/13 (Simon) - Updated displayed columns
2019/03/26 (Simon) - Changed page arguments
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="user=None, data=None, q=''"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/applications.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='applications'"/>
        </header>
        <section class="ui container">
            <h1 class="center title">Pending Applications</h1>
            <hr>
            % if (data is not None) and (len(data) > 0):
            <form method="get" action="" id="filter-form">
                <div class="ui icon input">
                  <input type="text" name="q" value="${q}"/ style="width:800px">
                  <i class="search icon"></i>
                </div>
                <button class ="ui secondary button" type="submit">Search</button>

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
                    <td><a href="view/${app['appID']}" class="ui secondary button">view</a></td>
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
            <div class="ui warning message">
                <i class="warning icon"></i>Database is empty.
            </div>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>