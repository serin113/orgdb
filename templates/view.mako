<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/13 (Simon) - Intial template code
2019/02/14 (Simon) - renamed to view.mako
2019/02/15 (Simon) - added <section> tags
                   - changed expected data type to dict from list
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="data=None, q=''"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/view.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">View All Affiliation Records</h1>
            <form method="get" action="" id="filter-form">
                <input type="text" name="q" value="${q}"/><button type="submit">search</button>
            </form>
            % if (data is not None) and (len(data) >= 0):
            <table>
                <tr>
                    <th></th>
                    <th></th>
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
            <h1>AffiliationRecordsTable is empty</h1>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>