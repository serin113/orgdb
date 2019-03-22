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
2019/03/23 (Simon) - Added table sorting
                   - Updated styling
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
        <script src="/scripts/tablesort.js"></script>
        <script>
            $(document).ready(function(){
                $('table').tablesort();
            });
        </script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="current='view'"/>
        </header>
        <section>
            <h1 class="center title">View All Affiliation Records</h1>
            
            % if (data is not None) and (len(data) > 0):
            <form method="get" action="" id="filter-form">
                <div class="ui action link icon input">
                  <input type="text" name="q" value="${q}"/ style="width:800px">
                  <button class="ui icon button" type="submit">
                      <i class="search icon"></i>
                  </button>
                </div>

            </form>
            <table class="ui compact unstackable selectable striped celled sortable blue table">
                <thead>
                    <tr>
                        <th data-vivaldi-spatnav-clickable="0"></th>
                        <th data-vivaldi-spatnav-clickable="1">club ID</th>
                        <th data-vivaldi-spatnav-clickable="1">club name</th>
                        <th data-vivaldi-spatnav-clickable="1">school</th>
                        <th data-vivaldi-spatnav-clickable="1">level</th>
                        <th data-vivaldi-spatnav-clickable="1">type</th>
                        <th data-vivaldi-spatnav-clickable="1">region</th>
                        <th data-vivaldi-spatnav-clickable="1">province</th>
                        <th data-vivaldi-spatnav-clickable="1">city</th>
                        <th data-vivaldi-spatnav-clickable="1">adviser/s</th>
                        <th data-vivaldi-spatnav-clickable="1">contact</th>
                        <th data-vivaldi-spatnav-clickable="1">email</th>
                        <th data-vivaldi-spatnav-clickable="1">last updated</th>
                    </tr>
                </thead>
                <tbody>
                    % for record in data:
                    <tr>
                        <td>
                            <a href="${record['clubID']}?q=${q}" class="ui basic button" id="view" style="margin:0">View</a>
                            <a href="/edit/${record['clubID']}" class="ui basic button" id="edit" style="margin:0">Edit</a>
                        </td>
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
                </tbody>
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