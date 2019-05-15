<%doc>
Created in 2019-03-06 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/06 (Simon) - Initial working code and documentation
2019/03/23 (Simon) - Changed region numbers from Roman to Arabic
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
2019/04/02 (Simon) - Updated form layout, moved some inline scripts to enable.js & apply.js
2019/04/05 (Simon) - If logged-in user is a club account, some elements are hidden from view
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
</%doc>


<%page args="user=None"/>
<%inherit file="_base.mako"/>


<%
if user is None:
    user = (None, -1)
ID, type = user
%>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/apply.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/enable.js"></script>
        <script src="/scripts/apply.js"></script>
        <title>PSYSC - Apply</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='apply'"/>
        </header>
        <div class="ui container">
            <h1 class="ui header center title">Application Form</h1>
            <div class="ui fluid raised blue container segment">
                <form method="post" action="insert" id="apply-form" class="ui form">
                    <div class="ui stackable grid">
                        % if type != 0:
                        <div class="sixteen wide column">
                            <div class="inline fields">
                                <label class="required">I am previously/currently affiliated with PSYSC</label>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="hasrecord" value="1" id="hasrecord-yes" required checked>
                                        <label for="hasrecord-yes">Yes</label>
                                    </div>
                                </div>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="hasrecord" value="0" id="hasrecord-no" required>
                                        <label for="hasrecord-no">No</label>
                                    </div>
                                </div>
                            </div>
                            <div class="ui hidden divider"></div>
                        </div>
                        <div class="sixteen wide blue column">
                            <h2 class="ui inverted header">Club Info</h2>
                        </div>
                        <div class="sixteen wide column" id="record_old">
                            <noscript>(this section only required if there's an existing record)</noscript>
                            <div class="required field">
                                <label>Club ID</label>
                                <input type="text" name="clubid" placeholder="Club ID">
                            </div>
                        </div>
                        <div class="sixteen wide column" id="record_new">
                            <div class="ui stackable grid">
                                <noscript>(this section only required if there's no existing record)</noscript>
                                <div class="sixteen wide column">
                                    <div class="required field">
                                        <label>Club Name</label>
                                        <input type="text" placeholder="Club Name" name="clubname">
                                    </div>
                                </div>
                                <div class="eight wide column">
                                    <div class="required field">
                                        <label>School</label>
                                        <input type="text" name="school" placeholder="School Name">
                                    </div>
                                </div>
                                <div class="four wide column">
                                    <div class="required field">
                                        <label>Type</label>
                                        <select class="ui fluid dropdown" name="type" id="type">
                                            <option value="1">Public</option>
                                            <option value="2">Private</option>
                                            <option value="3">State College/University</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="four wide column">
                                    <div class="required field">
                                        <label>Level/s</label>
                                        <select class="ui fluid dropdown" name="level" id="level">
                                            <option value="1">Elementary</option>
                                            <option value="2">High School</option>
                                            <option value="3">Elementary & High School</option>
                                            <option value="4">College</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="sixteen wide column">
                                    <div class="required field">
                                        <label>Address</label>
                                        <input type="text" placeholder="Address" name="address">
                                    </div>
                                </div>
                                <div class="six wide column">
                                    <div class="required field">
                                        <label>City</label>
                                        <input type="text" placeholder="City" name="city">
                                    </div>
                                </div>
                                <div class="six wide column">
                                    <div class="required field">
                                        <label>Province</label>
                                        <input type="text" placeholder="Province" name="province">
                                    </div>
                                </div>
                                <div class="four wide column">
                                    <div class="required field">
                                        <label>Region</label>
                                        <select class="ui fluid dropdown" name="region" id="region">
                                            <option value="1">1 (Ilocos)</option>
                                            <option value="2">2 (Cagayan Valley)</option>
                                            <option value="3">3 (Central Luzon)</option>
                                            <option value="4">4A (CALABARZON)</option>
                                            <option value="5">5 (Bicol)</option>
                                            <option value="6">6 (Western Visayas)</option>
                                            <option value="7">7 (Central Visayas)</option>
                                            <option value="8">8 (Eastern Visayas)</option>
                                            <option value="9">9 (Zamboanga Peninsula)</option>
                                            <option value="10">10 (Northern Mindanao)</option>
                                            <option value="11">11 (Davao)</option>
                                            <option value="12">12 (SOCCSKSARGEN)</option>
                                            <option value="13">13 (NCR)</option>
                                            <option value="14">14 (CAR)</option>
                                            <option value="15">15 (ARMM)</option>
                                            <option value="16">16 (CARAGA)</option>
                                            <option value="17">17 (MIMAROPA)</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="six wide column">
                                    <div class="required field">
                                        <label>Club Adviser/s</label>
                                        <input type="text" placeholder="Adviser Name" name="advisername">
                                    </div>
                                </div>
                                <div class="five wide column">
                                    <div class="required field">
                                        <label>Contact Number</label>
                                        <input type="text" placeholder="Contact No." name="contact">
                                    </div>
                                </div>
                                <div class="five wide column">
                                    <div class="required field">
                                        <label>E-mail</label>
                                        <input type="email" placeholder="Email Address" name="email">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="sixteen wide column"></div>
                        % else:
                        <input type="hidden" name="hasrecord" value="1" required>
                        <input type="hidden" name="clubid" value="${ID}" required>
                        % endif
                        <div class="sixteen wide blue column">
                            <h2 class="ui inverted header">Affiliation Info</h2>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>School Year</label>
                                <input type="number"  name="schoolyear" min="2007" max="2050" value = "2007" required>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Number of years paid</label>
                                <input type="number"  name="yearsaffiliated" min="1" value = "1" required>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Number of club advisers</label>
                                <input type="number" name="sca" min="1" required>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Number of club members</label>
                                <input type="number"  name="scm" min="1" required>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Payment Amount</label>
                                <input type="number"  name="paymentamount" min="0">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Mode of Payment</label>
                                <input type="text" placeholder="Payment Mode" name="paymentmode">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Payment Date</label>
                                <input type="date" name="paymentdate">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Payment Identifier</label>
                                <input type="text" placeholder="Payment ID" name="paymentid">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Receipt Number</label>
                                <input type="text" placeholder="Receipt #" name="receiptnumber">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Payment Delivery Mode</label>
                                <input type="text" placeholder="Payment Delivery Mode" name="paymentsendmode">
                            </div>
                        </div>
                        <div class="ui horizontal divider"></div>
                        <div class="sixteen wide column">
                            <button class='ui submit blue button' type="submit">Apply</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <footer>
            <%include file="_footer.mako"/>
        </footer>
    </body>
</html>