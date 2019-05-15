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
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
                   - Added return button
                   - Template accepts "q" parameter
                   - Added affiliation list table
</%doc>


<%doc>
Mako variables:
    - (dict type) record_info
    - (list type) affiliations
        - (dict type) affiliation
</%doc>


<%page args="user=None, record_info=None, affiliations=[], q=''"/>
<%inherit file="_base.mako"/>


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
        <script src="/scripts/back.js"></script>
        <script src="/scripts/tablesort.js"></script>
        <script src="/scripts/enable_tablesort.js"></script>
        <title>
            % if record_info is not None:
            PSYSC - ${record_info["clubName"]}
            % else:
            PSYSC
            % endif
        </title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='view'"/>
        </header>
        <div class="ui container">
            % if type == 1 or type == 2:
            <div class="ui container">
                % if len(q) > 0:
                <a href="/view?q=${q}" class="ui small basic blue button" id="button">< Back to Records</a>
                % else:
                <a href="/view" class="ui small basic blue button" id="button">< Back to Records</a>
                % endif
            </div>
            % endif
            % if record_info is not None:
            <div class="ui inverted blue raised vertical segments">
                <div class="ui inverted blue clearing segment">
                    % if type == 1 or type == 2:
                    % if len(q) > 0:
                    <a href="/edit/${record_info['clubID']}?q=${q}" class="ui right floated blue icon button" tabindex="0">
                        <i class="edit icon"></i>
                    </a>
                    % else:
                    <a href="/edit/${record_info['clubID']}" class="ui right floated blue icon button" tabindex="0">
                        <i class="edit icon"></i>
                    </a>
                    % endif
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
                % if affiliations is not None:
                <div class="ui segment">
                    <div class="ui attached container" style="overflow-x:auto">
                        <table class="ui selectable stackable compact striped celled sortable blue small table">
                            <thead class="full-width">
                                <tr>
                                    <th data-vivaldi-spatnav-clickable="1">school year/s</th>
                                    <th data-vivaldi-spatnav-clickable="1">years paid</th>
                                    <th data-vivaldi-spatnav-clickable="1">adviser/s</th>
                                    <th data-vivaldi-spatnav-clickable="1">members</th>
                                    <th data-vivaldi-spatnav-clickable="1">paid through</th>
                                    <th data-vivaldi-spatnav-clickable="1">date paid</th>
                                    <th data-vivaldi-spatnav-clickable="1">payment ID</th>
                                    <th data-vivaldi-spatnav-clickable="1">paid amount</th>
                                    <th data-vivaldi-spatnav-clickable="1">receipt number</th>
                                    <th data-vivaldi-spatnav-clickable="1">paid sent through</th>
                                    <th data-vivaldi-spatnav-clickable="1">benefits</th>
                                    <th data-vivaldi-spatnav-clickable="1">remarks</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for aff in affiliations:
                                <tr>
                                    <td>${"{} - {}".format(int(aff["schoolYear"]) - 1, int(aff["schoolYear"]) - 1 + int(aff["yearsAffiliated"]))}</td>
                                    <td>${aff["yearsAffiliated"]}</td>
                                    <td>${aff["SCA"]}</td>
                                    <td>${aff["SCM"]}</td>
                                    <td class="collapsing">${aff["paymentMode"]}</td>
                                    <td class="collapsing">${aff["paymentDate"]}</td>
                                    <td class="collapsing">${aff["paymentID"]}</td>
                                    <td class="collapsing">${aff["paymentAmount"]}</td>
                                    <td class="collapsing">${aff["receiptNumber"]}</td>
                                    <td class="collapsing">${aff["paymentSendMode"]}</td>
                                    <td class="collapsing">${aff["benefits"]}</td>
                                    <td class="right aligned collapsing">${aff["remarks"]}</td>
                                </tr>
                                % endfor
                            </tbody>
                        </table>
                    </div>
                </div>
                % endif
                <div class="ui secondary segment">
                    <i>Last updated ${record_info["dateUpdated"]}</i>
                </div>
            </div>
            % else:
            <div class="ui warning message">
                <i class="warning icon"></i>Record doesn't exist.
            </div>
            % endif
        </div>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>