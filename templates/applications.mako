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
2019/04/24 (Simon) - Updated template, added region/level/type conversion to readable string
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
                   - Resized search bar
</%doc>


<%doc>
Mako variables:
    - (dict type) data
</%doc>


<%page args="user=None, data=None, q=''"/>
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
        <script src="/scripts/tablesort.js"></script>
        <script src="/scripts/enable_tablesort.js"></script>
        <title>PSYSC - Applications</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='applications'"/>
        </header>
        <div class="ui center aligned container">
            <h1 class="ui header title">Pending Applications</h1>
            <form method="get" action="" id="filter-form">
                <div class="ui action icon input">
                  <input type="text" name="q" value="${q}" placeholder="Search..."/>
                    % if len(q) > 0:
                    <a href="/applications" class="ui button" tabindex="0">Reset</a>
                    % endif
                    <button class ="ui icon button" type="submit"><i class="search icon"></i></button>
                </div>
            </form>
            % if (data is not None):
            % if len(data) > 0:
            <div class="ui left aligned container">
                % for app in data:
                <div class="ui inverted blue raised vertical segments">
                    <div class="ui inverted blue segment">
                        <div class="ui right floated small buttons">
                            <a href="approve/${app['appID']}" class="ui positive vertical animated button">
                                <div class="visible content">approve</div>
                                <div class="hidden content"><i class="check icon"></i></div>
                            </a>
                            <a href="reject/${app['appID']}" class="ui negative vertical animated button">
                                <div class="visible content">reject</div>
                                <div class="hidden content"><i class="close icon"></i></div>
                            </a>
                        </div>
                        <h1 class="ui inverted left floated header">
                            ${app["clubName"]}
                            <div class="ui inverted sub header">${app["school"]}</div>
                        </h1>
                        <div class="ui hidden clearing fitted divider"></div>
                        <div class="ui horizontal list">
                            <div class="item">
                                <div class="ui green label">
                                    ${regionName[app["region"]][1]}
                                    <div class="detail">Region ${regionName[app["region"]][0]}</div>
                                </div>
                            </div>
                            <div class="item">
                                <div class="ui violet label">
                                    ${levelName[app["level"]]}
                                    <div class="detail">Level</div>
                                </div>
                            </div>
                            <div class="item">
                                <div class="ui teal label">
                                    ${typeName[app["type"]]}
                                    <div class="detail">Type</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ui segment">
                        <div class="ui stackable grid">
                            <div class="eight wide column">
                                <div class="ui list">
                                    <div class="item"><b>School Year: </b>${app["schoolYear"]-1} - ${app["schoolYear"]}</div>
                                    <div class="item"><b>Years Paid: </b>${app["yearsAffiliated"]}</div>
                                    <div class="item"><b>Number of Club Advisers: </b>${app["SCA"]}</div>
                                    <div class="item"><b>Number of Club Members: </b>${app["SCM"]}</div>
                                </div>
                            </div>
                            <div class="eight wide column">
                                <div class="ui list">
                                    <div class="item"><b>Paid Amount: </b>${app["paymentAmount"]}</div>
                                    <div class="item"><b>Payment ID: </b>${app["paymentID"]}</div>
                                    <div class="item"><b>Receipt Number: </b>${app["receiptNumber"]}</div>
                                    <div class="item"><b>Mode of Payment: </b>${app["paymentMode"]}</div>
                                    <div class="item"><b>Payment Sent Thru: </b>${app["paymentSendMode"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ui segment">
                        <div class="ui stackable grid">
                            <div class="eight wide column">
                                <div class="ui list">
                                    <div class="item"><b>Club Adviser/s: </b>${app["adviserName"]}</div>
                                    <div class="item"><b>Contact: </b>${app["contact"]}</div>
                                    <div class="item"><b>E-mail: </b><a href="mailto:${app['email']}">${app["email"]}</a></div>
                                </div>
                            </div>
                            <div class="eight wide column">
                                <div class="ui list">
                                    <div class="item"><b>Address: </b>${app["address"]}</div>
                                    <div class="item"><b>City: </b>${app["city"]}</div>
                                    <div class="item"><b>Province: </b>${app["province"]}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="ui secondary segment">
                        <i>Application sent ${app["dateCreated"]}</i>
                    </div>
                </div>
                % endfor
            </div>
            % else:
            <div class="ui warning message">
                <i class="warning icon"></i>No pending applications.
            </div>
            % endif
            % endif
        </div>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>