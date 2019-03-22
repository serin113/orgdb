<%doc>
Created in 2019-03-15 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/15 (Simon) - Initial template
2019/03/23 (Simon) - Added tables per school year
</%doc>


<%doc>
Mako variables:
    (dict) data: {schoolYear: totals}
        - (list) totals
            - 0: (dict) regionTotals: {region: total}
            - 1: (dict) levelTotals: {level: total}
            - 2: (dict) typeTotals: {type: total}
</%doc>


<%page args="data=None"/>


<%
regionName = {
    1: "I (Ilocos)",
	2: "II (Cagayan Valley)",
	3: "III (Central Luzon)",
	4: "IV-A (CALABARZON)",
	5: "V (Bicol)",
	6: "VI (Western Visayas)",
	7: "VII (Central Visayas)",
	8: "VIII (Eastern Visayas)",
	9: "IX (Zamboanga Peninsula)",
	10: "X (Northern Mindanao)",
	11: "XI (Davao)",
	12: "XII (SOCCSKSARGEN)",
	13: "XIV (NCR)",
	14: "XV (CAR)",
	15: "XVI (ARMM)",
	16: "XII (CARAGA)",
	17: "XVII (MIMAROPA)"
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
        <link rel="stylesheet" href="/styles/index.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1>Affiliated clubs per school year</h1>
            % if data is not None:
            % for year, totals in data.items():
            <hr>
            <h2>${year-1}-${year}</h2>
            <h3>
            <table>
                <tr>
                    <th>region</th>
                    <th>total</th>
                </tr>
                % for region, total in totals[0].items():
                <tr>
                    <td>${regionName[region]}</td>
                    <td>${total}</td>
                </tr>
                % endfor
            </table>
            <br>
            <table>
                <tr>
                    <th>level</th>
                    <th>total</th>
                </tr>
                % for level, total in totals[1].items():
                <tr>
                    <td>${levelName[level]}</td>
                    <td>${total}</td>
                </tr>
                % endfor
            </table>
            <br>
            <table>
                <tr>
                    <th>type</th>
                    <th>total</th>
                </tr>
                % for type, total in totals[2].items():
                <tr>
                    <td>${typeName[type]}</td>
                    <td>${total}</td>
                </tr>
                % endfor
            </table>
            % endfor
            % else
            <p class="center">Database is empty</p>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>