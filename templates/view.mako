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
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/27 (Simon) - Added reset button for search bar
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
                   - Updated table styling
                   - Translates region/level/type numbers to readable strings
2019/04/02 (Simon) - Updated button styles, moved some inline scripts to enable_tablesort.js
2019/04/23 (Simon) - Changed handling of empty results
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="user=None, data=None, q=''"/>


<%
regionName = {
    1: "1 (Ilocos)",
	2: "2 (Cagayan Valley)",
	3: "3 (Central Luzon)",
	4: "4A (CALABARZON)",
	5: "5 (Bicol)",
	6: "6 (W. Visayas)",
	7: "7 (C. Visayas)",
	8: "8 (E. Visayas)",
	9: "9 (Zamboanga Peninsula)",
	10: "10 (N. Mindanao)",
	11: "11 (Davao)",
	12: "12 (SOCCSKSARGEN)",
	13: "13 (NCR)",
	14: "14 (CAR)",
	15: "15 (ARMM)",
	16: "16 (CARAGA)",
	17: "17 (MIMAROPA)"
}
levelName = {
    1: "Elementary",
    2: "High School",
    3: "Elementary & H.S.",
    4: "College"
}
typeName = {
    1: "Public",
    2: "Private",
    3: "State College/University"
}
%>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/view.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/tablesort.js"></script>
        <script src="/scripts/enable_tablesort.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='view'"/>
        </header>
        <h1 class="ui header center title">View All Affiliation Records</h1>
        <div class="ui container">
            <form method="get" action="" id="filter-form">
                <div class="ui fluid action icon input">
                  <input type="text" name="q" value="${q}" placeholder="Search..."/>
                  % if len(q) > 0:
                  <a href="/view" class="ui button" tabindex="0">Reset</a>
                  % endif
                  <button class="ui icon button" type="submit">
                      <i class="search icon"></i>
                  </button>
                </div>
            </form>
            % if (data is not None):
            % if len(data) > 0:
            <div class="ui container" style="overflow-x:auto">
                <table class="ui selectable stackable compact striped celled sortable blue small table">
                    <thead class="full-width">
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
                            <td class="collapsing center aligned">
                                <div class="ui two small icon buttons">
                                    % if len(q) > 0:
                                    <a href="${record['clubID']}?q=${q}" class="ui primary button" tabindex="0">
                                        <i class="eye icon"></i>
                                    </a>
                                    % else:
                                    <a href="${record['clubID']}" class="ui primary button" tabindex="0">
                                        <i class="eye icon"></i>
                                    </a>
                                    % endif
                                    <a href="/edit/${record['clubID']}" class="ui button" tabindex="0">
                                        <i class="edit icon"></i>
                                    </a>
                                </div>
                            </td>
                            <td>${record['clubID']}</td>
                            <td class="collapsing">${record['clubName']}</td>
                            <td class="collapsing">${record['school']}</td>
                            <td class="collapsing">${levelName[record['level']]}</td>
                            <td class="collapsing">${typeName[record['type']]}</td>
                            <td class="collapsing">${regionName[record['region']]}</td>
                            <td>${record['province']}</td>
                            <td>${record['city']}</td>
                            <td>${record['adviserName']}</td>
                            <td class="collapsing">${record['contact']}</td>
                            <td class="collapsing"><a href="mailto:${record['email']}">${record['email']}</a></td>
                            <td class="right aligned collapsing">${record['dateUpdated']}</td>
                        </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
            % else:
            <div class="ui warning message">
                <i class="warning icon"></i>Zero results.
            </div>
            % endif
            % endif
        </div>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>