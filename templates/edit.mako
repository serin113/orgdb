<%doc>
Created in 2019-03-29 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/29 (Simon) - Initial working code
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
                   - Added return button
                   - Template accepts "q" parameter
</%doc>


<%doc>
Mako variables:
    - (dict type) record_info
</%doc>


<%page args="user=None, record_info=None, q=''"/>
<%inherit file="_base.mako"/>


<%
from collections import defaultdict
type_sel = defaultdict(lambda:"")
region_sel = defaultdict(lambda:"")
level_sel = defaultdict(lambda:"")
if record_info is not None:
    type_sel[str(record_info["type"])] = "selected"
    region_sel[str(record_info["region"])] = "selected"
    level_sel[str(record_info["level"])] = "selected"
%>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/add.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/enable.js"></script>
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
        <section class="ui center aligned container">
            <div class="ui left aligned container">
                % if len(q) > 0:
                <a href="/view?q=${q}" class="ui small basic blue button" id="button">< Back to Records</a>
                % else:
                <a href="/view" class="ui small basic blue button" id="button">< Back to Records</a>
                % endif
            </div>
            <h1 class="ui header title">Edit Affiliation Record</h1>
            % if record_info is not None:
            <div class="ui fluid raised blue left aligned container segment">
                <form method="post" action="update" id="add-form" class="ui form">
                    <div class="ui stackable grid">
                        <div class="ui sixteen wide blue column">
                            <h1 class="ui inverted header">
                                ${record_info["clubName"]}
                                <div class="ui inverted sub header">${record_info["school"]}</div>
                            </h1>
                        </div>
                        <div class="sixteen wide column">
                            <div class="required field">
                                <label>Club Name</label>
                                <input type="text" placeholder="Club Name" name="clubname" value="${record_info['clubName']}" required>
                            </div>
                        </div>
                        <div class="eight wide column">
                            <div class="required field">
                                <label>School</label>
                                <input type="text" name="school" required placeholder="School Name" value="${record_info['school']}">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Type</label>
                                <select class="ui fluid dropdown" name="type" id="type" required>
                                    <option value="1" ${type_sel["1"]}>Public</option>
                                    <option value="2" ${type_sel["2"]}>Private</option>
                                    <option value="3" ${type_sel["3"]}>State College/University</option>
                                </select>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Level/s</label>
                                <select class="ui fluid dropdown" name="level" id="level" required>
                                    <option value="1" ${level_sel["1"]}>Elementary</option>
                                    <option value="2" ${level_sel["2"]}>High School</option>
                                    <option value="3" ${level_sel["3"]}>Elementary & High School</option>
                                    <option value="4" ${level_sel["4"]}>College</option>
                                </select>
                            </div>
                        </div>
                        <div class="sixteen wide column">
                            <div class="required field">
                                <label>Address</label>
                                <input type="text" placeholder="Address" name="address" required value="${record_info['address']}">
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>City</label>
                                <input type="text" placeholder="City" name="city" required value="${record_info['city']}">
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>Province</label>
                                <input type="text" placeholder="Province" name="province" required value="${record_info['province']}">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Region</label>
                                <select class="ui fluid dropdown" name="region" id="region" required>
                                    <option value="1" ${level_sel["1"]}>1 (Ilocos)</option>
                                    <option value="2" ${level_sel["2"]}>2 (Cagayan Valley)</option>
                                    <option value="3" ${level_sel["3"]}>3 (Central Luzon)</option>
                                    <option value="4" ${level_sel["4"]}>4A (CALABARZON)</option>
                                    <option value="5" ${level_sel["5"]}>5 (Bicol)</option>
                                    <option value="6" ${level_sel["6"]}>6 (Western Visayas)</option>
                                    <option value="7" ${level_sel["7"]}>7 (Central Visayas)</option>
                                    <option value="8" ${level_sel["8"]}>8 (Eastern Visayas)</option>
                                    <option value="9" ${level_sel["9"]}>9 (Zamboanga Peninsula)</option>
                                    <option value="10" ${level_sel["10"]}>10 (Northern Mindanao)</option>
                                    <option value="11" ${level_sel["11"]}>11 (Davao)</option>
                                    <option value="12" ${level_sel["12"]}>12 (SOCCSKSARGEN)</option>
                                    <option value="13" ${level_sel["13"]}>13 (NCR)</option>
                                    <option value="14" ${level_sel["14"]}>14 (CAR)</option>
                                    <option value="15" ${level_sel["15"]}>15 (ARMM)</option>
                                    <option value="16" ${level_sel["16"]}>16 (CARAGA)</option>
                                    <option value="17" ${level_sel["17"]}>17 (MIMAROPA)</option>
                                </select>
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>Club Adviser/s</label>
                                <input type="text" placeholder="Adviser Name" name="advisername" required value="${record_info['adviserName']}">
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required field">
                                <label>Contact Number</label>
                                <input type="text" placeholder="Contact No." name="contact" required value="${record_info['contact']}">
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required field">
                                <label>E-mail</label>
                                <input type="email" placeholder="Email Address" name="email" required value="${record_info['email']}">
                            </div>
                        </div>
                        <div class="ui horizontal hidden divider"></div>
                        <div class="sixteen wide column">
                            <button class='ui blue submit button' type="submit">Update Record</button>
                        </div>
                    </div>
                </form>
            </div>
            % endif
        </section>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>