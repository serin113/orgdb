<%doc>
Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/23 (Simon) - Intial template code
2019/03/26 (Simon) - Changed page arguments, updated UI
</%doc>


<%doc>
Mako variables:
    - (dict type) record_info
    - (list type) affiliations
        - (dict type) affiliation
</%doc>


<%page args="user=None, record_info=None, affiliations=[]"/>


<%
regionName = {
    1: ("1", "Ilocos"),
	2: ("2", "Cagayan Valley"),
	3: ("3", "Central Luzon"),
	4: ("4A", "CALABARZON"),
	5: ("5", "Bicol"),
	6: ("6", "Western Visayas"),
	7: ("7", "Central Visayas"),
	8: ("8", "Eastern Visayas"),
	9: ("9", "Zamboanga Peninsula"),
	10: ("10", "Northern Mindanao"),
	11: ("11", "Davao"),
	12: ("12", "SOCCSKSARGEN"),
	13: ("13", "NCR"),
	14: ("14", "CAR"),
	15: ("15", "ARMM"),
	16: ("16", "CARAGA"),
	17: ("17", "MIMAROPA")
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
        <link rel="stylesheet" href="/styles/applications.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='view'"/>
        </header>
        <section class="ui container">
            % if record_info is not None:
            <div class="ui inverted blue raised vertical segments">
                <div class="ui inverted blue segment">
                    <h1 class="ui inverted header">
                        ${record_info["clubName"]}
                        <div class="ui inverted sub header">${record_info["school"]}</div>
                    </h1>
                    <div class="ui green label">
                        ${regionName[record_info["region"]][1]}
                        <div class="detail">${regionName[record_info["region"]][0]}</div>
                    </div>
                    <div class="ui violet label">
                        ${levelName[record_info["level"]]}
                        <div class="detail">Level</div>
                    </div>
                    <div class="ui teal label">
                        ${typeName[record_info["type"]]}
                        <div class="detail">Type</div>
                    </div>
                </div>
                <div class="ui basic segment">
                    ${record_info["clubID"]}<br>
                    ${record_info["dateUpdated"]}<br>
                    ${record_info["address"]}<br>
                    ${record_info["city"]}<br>
                    ${record_info["province"]}<br>
                    ${record_info["adviserName"]}<br>
                    ${record_info["contact"]}<br>
                    ${record_info["email"]}
                </div>
            </div>
            % endif
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>