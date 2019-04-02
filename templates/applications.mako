<%doc>
Created in 2019-03-12 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/12 (Simon) - Intial template code
2019/03/13 (Simon) - Updated displayed columns
2019/03/26 (Simon) - Changed page arguments
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
                   - Removed appID column
                   - Updated table styling, added sorting
2019/04/02 (Simon) - Updated form layout, moved some inline scripts to enable_tablesort.js
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="user=None, data=None, q=''"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/applications.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/tablesort.js"></script>
        <script src="/scripts/enable_tablesort.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='applications'"/>
        </header>
        <h1 class="ui header center title">Pending Applications</h1>
        <div class="ui container">
            <form method="get" action="" id="filter-form">
                <div class="ui fluid action icon input">
                  <input type="text" name="q" value="${q}" placeholder="Search..."/>
                    % if len(q) > 0:
                    <a href="/applications" class="ui button" tabindex="0">Reset</a>
                    % endif
                    <button class ="ui icon button" type="submit"><i class="search icon"></i></button>
                </div>
            </form>
            % if (data is not None) and (len(data) > 0):
            <div class="ui container" style="overflow-x:auto">
                <table class="ui selectable stackable compact striped celled sortable blue small table">
                    <thead class="full-width">
                        <tr>
                            <th data-vivaldi-spatnav-clickable="0"></th>
                            <th data-vivaldi-spatnav-clickable="1">club name</th>
                            <th data-vivaldi-spatnav-clickable="1">school</th>
                            <th data-vivaldi-spatnav-clickable="1">adviser/s</th>
                            <th data-vivaldi-spatnav-clickable="1">payment amount</th>
                            <th data-vivaldi-spatnav-clickable="1">payment date</th>
                            <th data-vivaldi-spatnav-clickable="1">contact</th>
                            <th data-vivaldi-spatnav-clickable="1">email</th>
                            <th data-vivaldi-spatnav-clickable="1">last updated</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for app in data:
                        <tr>
                            <td class="collapsing center aligned">
                                <div class="ui small buttons">
                                    <a href="view/${app['appID']}" class="ui icon primary button"><i class="eye icon"></i></a>
                                    <a href="approve/${app['appID']}" class="ui positive vertical animated button">
                                        <div class="visible content">approve</div>
                                        <div class="hidden content"><i class="check icon"></i></div>
                                    </a>
                                    <a href="reject/${app['appID']}" class="ui negative vertical animated button">
                                        <div class="visible content">reject</div>
                                        <div class="hidden content"><i class="close icon"></i></div>
                                    </a>
                                </div>
                            </td>
                            <td class="collapsing">${app['clubName']}</td>
                            <td class="collapsing">${app['school']}</td>
                            <td>${app['adviserName']}</td>
                            <td class="collapsing">${app['paymentAmount']}</td>
                            <td class="collapsing">${app['paymentDate']}</td>
                            <td class="collapsing">${app['contact']}</td>
                            <td><a href="mailto:${app['email']}">${app['email']}</a></td>
                            <td>${app['dateCreated']}</td>
                        </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
            <%doc>
            <div class="ui container">
                % for app in data:
                <div class="ui inverted blue raised vertical segments">
                    <div class="ui blue segment">
                        <h1 class="ui blue header">
                            ${app["clubName"]}
                            <div class="ui blue sub header">${app["school"]}</div>
                        </h1>
                        <div class="ui small buttons">
                            <a href="view/${app['appID']}" class="ui icon primary button"><i class="eye icon"></i></a>
                            <a href="approve/${app['appID']}" class="ui positive vertical animated button">
                                <div class="visible content">approve</div>
                                <div class="hidden content"><i class="check icon"></i></div>
                            </a>
                            <a href="reject/${app['appID']}" class="ui negative vertical animated button">
                                <div class="visible content">reject</div>
                                <div class="hidden content"><i class="close icon"></i></div>
                            </a>
                        </div>
                    </div>
                </div>
                % endfor
            </div>
            </%doc>
            % else:
            <div class="ui warning message">
                <i class="warning icon"></i>Database is empty.
            </div>
            % endif
        </div>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>