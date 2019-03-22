<%doc>
Created in 2019-03-15 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/15 (Simon) - Initial template
2019/03/23 (Simon) - Added tables per school year
                   - Added table sorting
                   - Updated styling
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


<%page args="data=None"/>


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
        <link href="/styles/index.css" rel="stylesheet"/>
        <link href="/styles/semantic.min.css" rel="stylesheet" type="text/css">
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
            <%include file="header.mako" args="current='summary'"/>
        </header>
        <section>
            <h1 class="center title">Affiliated clubs per school year</h1>
            % if data is not None:
            <div class="ui container">
                % for year, totals in data.items():
                <div class="ui horizontal divider"></div>
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
                    <div class="ui horizontal segments">
                        <div class="ui segment">
                            <table class="ui single line striped sortable fixed unstackable compact blue table">
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
                        <div class="ui segment">
                            <table class="ui single line striped sortable fixed unstackable compact blue table">
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
                        <div class="ui segment">
                            <table class="ui single line striped sortable fixed unstackable compact blue table">
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
                    % endif
                </div>
                % endfor
            </div>
            % else:
            <p class="center">Database is empty</p>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>