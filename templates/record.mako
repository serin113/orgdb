<%doc>
Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/23 (Simon) - Intial template code
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
2019/04/02 (Simon) - Updated layout
2019/04/23 (Simon) - Updated layout, added edit button (visible if admin)
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

if user is None:
    user = (None, -1)
ID, type = user
%>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/applications.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='view'"/>
        </header>
        <div class="ui container">
            % if record_info is not None:
            <div class="ui inverted blue raised vertical segments">
                <div class="ui inverted blue clearing segment">
                    % if type == 1:
                    <a href="/edit/${record_info['clubID']}" class="ui right floated blue icon button" tabindex="0">
                        <i class="edit icon"></i>
                    </a>
                    <h1 class="ui inverted left floated header">
                    % else:
                    <h1 class="ui inverted header">
                    % endif
                        ${record_info["clubName"]}
                        <div class="ui inverted sub header">${record_info["school"]}</div>
                    </h1>
                    <div class="ui hidden clearing fitted divider"></div>
                    <div class="ui horizontal list">
                        <div class="item">
                            <div class="ui green label">
                                ${regionName[record_info["region"]][1]}
                                <div class="detail">Region ${regionName[record_info["region"]][0]}</div>
                            </div>
                        </div>
                        <div class="item">
                            <div class="ui violet label">
                                ${levelName[record_info["level"]]}
                                <div class="detail">Level</div>
                            </div>
                        </div>
                        <div class="item">
                            <div class="ui teal label">
                                ${typeName[record_info["type"]]}
                                <div class="detail">Type</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="ui segment">
                    <div class="ui stackable grid">
                        <div class="eight wide column">
                            <div class="ui list">
                                <div class="item"><b>Club Adviser/s: </b>${record_info["adviserName"]}</div>
                                <div class="item"><b>Contact: </b>${record_info["contact"]}</div>
                                <div class="item"><b>E-mail: </b><a href="mailto:${record_info['email']}">${record_info["email"]}</a></div>
                            </div>
                        </div>
                        <div class="eight wide column">
                            <div class="ui list">
                                <div class="item"><b>Address: </b>${record_info["address"]}</div>
                                <div class="item"><b>City: </b>${record_info["city"]}</div>
                                <div class="item"><b>Province: </b>${record_info["province"]}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="ui secondary segment">
                    <i>Last updated ${record_info["dateUpdated"]}</i>
                </div>
            </div>
            % endif
        </div>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>