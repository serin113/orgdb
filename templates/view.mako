<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/13 (Simon) - Intial template code
2019/02/14 (Simon) - renamed to view.mako
2019/02/15 (Simon) - added <section> tags
                   - changed expected data type to dict from list
2019/03/07 (Simon) - Added clubID column
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="data=None, q=''"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/view.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">View All Affiliation Records</h1>
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
                    <th>club ID</th>
                    <th>club name</th>
                    <th>school</th>
                    <th>level</th>
                    <th>type</th>
                    <th>region</th>
                    <th>province</th>
                    <th>city</th>
                    <th>adviser/s</th>
                    <th>contact</th>
                    <th>email</th>
                    <th>last updated</th>
                </tr>
                % for record in data:
                <tr>
                    <td><a href="${record['clubID']}?q=${q}">view</a></td>
                    <td>edit</td>
                    <td>${record['clubID']}</td>
                    <td>${record['clubName']}</td>
                    <td>${record['school']}</td>
                    <td>${record['level']}</td>
                    <td>${record['type']}</td>
                    <td>${record['region']}</td>
                    <td>${record['province']}</td>
                    <td>${record['city']}</td>
                    <td>${record['adviserName']}</td>
                    <td>${record['contact']}</td>
                    <td><a href="mailto:${record['email']}">${record['email']}</a></td>
                    <td>${record['dateUpdated']}</td>
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