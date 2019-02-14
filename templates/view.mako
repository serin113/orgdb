<%doc>
Created in 2019-02-08 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/13 - Intial template code
2019/02/14 - renamed to view.mako
</%doc>


<%doc>
Mako variables:
    (dict type) data
</%doc>


<%page args="data=None"/>


<html>
    <head>
        <link rel="stylesheet" href="/styles/view.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        % if (data is None) or (len(data) == 0):
        <h1>AffiliationRecordsTable is empty</h1>
        % else:
        <table>
            <tr>
                <th>club name</th>
                <th>school</th>
                <th>region</th>
                <th>contact</th>
                <th>email</th>
                <th>last updated</th>
            </tr>
            % for record in data:
            <tr>
                <td><a href="r/${record[-1]}">${record[0]}</a></td>
                <td>${record[1]}</td>
                <td>${record[2]}</td>
                <td>${record[3]}</td>
                <td><a href="mailto:${record[4]}">${record[4]}</a></td>
                <td>${record[5]}</td>
            </tr>
            % endfor
        </table>
        % endif
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>