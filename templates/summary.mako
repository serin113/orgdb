<%doc>
Created in 2019-03-15 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/15 (Simon) - Initial template
2019/03/23 (Simon) - Added tables per school year
                   - Added table sorting
                   - Updated styling
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/27 (Simon) - Added filter bar
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
                   - Updated table styling
2019/04/02 (Simon) - Updated table styling, moved some inline scripts to enable_tablesort.js
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
</%doc>


<%doc>
Mako variables:
    (dict) data: {schoolYear: totals}
        - (list) totals
            - 0: (dict) regionTotals: {region: total}
            - 1: (dict) levelTotals: {level: total}
            - 2: (dict) typeTotals: {type: total}
            - 3: (int) overallTotal
</%doc>


<%page args="user=None, data=None, q=''"/>
<%inherit file="_base.mako"/>


<%
regionName = {
    1: "1 (Ilocos)",
	2: "2 (Cagayan Valley)",
	3: "3 (Central Luzon)",
	4: "4A (CALABARZON)",
	5: "5 (Bicol)",
	6: "6 (Western Visayas)",
	7: "7 (Central Visayas)",
	8: "8 (Eastern Visayas)",
	9: "9 (Zamboanga Peninsula)",
	10: "10 (Northern Mindanao)",
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
        <link href="/styles/index.css" rel="stylesheet"/>
        <link href="/styles/semantic.min.css" rel="stylesheet" type="text/css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/tablesort.js"></script>
        <script src="/scripts/enable_tablesort.js"></script>
        <title>PSYSC - Summary</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='summary'"/>
        </header>
        <section class="ui center aligned container">
            <h1 class="center title">Affiliated clubs per school year</h1>
            <form method="get" action="" id="filter-form">
                <div class="ui action icon input">
                  <input type="number"  name="q" min="2007" max="2050" value = "${q}" placeholder="YYYY"/>
                  % if len(q) > 0:
                  <a href="/summary" class="ui button">Reset</a>
                  % endif
                  <button class="ui icon button" type="submit">
                      <i class="search icon"></i>
                  </button>
                </div>
            </form>
            % if data is not None:
            % for year, totals in data.items():
            <div class="ui raised segments">
                <div class="ui horizontal segments">
                    <div class="ui right aligned inverted blue segment">
                        <h1 class="ui header">${year-1}-${year}</h1>
                    </div>
                    <div class="ui left aligned inverted blue secondary segment">
                        <div class="ui tiny horizontal inverted statistic">
                            <div class="value">${totals[3]}</div>
                            <div class="label">Affiliated Club/s</div>
                        </div>
                    </div>
                </div>
                % if totals[3] > 0:
                <div class="ui padded stackable grid">
                    <div class="three column row">
                        <div class="column">
                            <table class="ui striped sortable unstackable compact blue table">
                                <thead>
                                    <tr>
                                        <th data-vivaldi-spatnav-clickable="1">region</th>
                                        <th data-vivaldi-spatnav-clickable="1">total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % for region, total in totals[0].items():
                                    <tr>
                                        <td data-label="region">${regionName[region]}</td>
                                        <td data-label="total">${total}</td>
                                    </tr>
                                    % endfor
                                </tbody>
                            </table>
                        </div>
                        <div class="column">
                            <table class="ui striped sortable unstackable compact blue table">
                                <thead>
                                    <tr>
                                        <th data-vivaldi-spatnav-clickable="1">level</th>
                                        <th data-vivaldi-spatnav-clickable="1">total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % for level, total in totals[1].items():
                                    <tr>
                                        <td data-label="level">${levelName[level]}</td>
                                        <td data-label="total">${total}</td>
                                    </tr>
                                    % endfor
                                </tbody>
                            </table>
                        </div>
                        <div class="column">
                            <table class="ui striped sortable unstackable compact blue table">
                                <thead>
                                    <tr>
                                        <th data-vivaldi-spatnav-clickable="1">type</th>
                                        <th data-vivaldi-spatnav-clickable="1">total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % for type, total in totals[2].items():
                                    <tr>
                                        <td data-label="type">${typeName[type]}</td>
                                        <td data-label="total">${total}</td>
                                    </tr>
                                    % endfor
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                % endif
            </div>
            % endfor
            % else:
            <div class="ui warning message">
                <i class="warning icon"></i>Database is empty.
            </div>
            % endif
        </section>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>