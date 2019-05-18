<%doc>
Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/06 (Simon) - Initial working code and documentation
2019/02/13 (Simon) - Added Mako templating
2019/02/14 (Simon) - renamed to add.mako
2019/02/15 (Simon) - added <section> tags
2019/03/15 (Nathan)- finished adding semantic-ui
2019/03/23 (Simon) - Changed region numbers from Roman to Arabic
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/27 (Simon) - Changed max value for "schoolyear" to 2050
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
                   - Updated form layout
2019/04/02 (Simon) - Updated form layout, moved some inline scripts to enable.js
2019/05/15 (Simon) - Template inherits _base.mako for whitespace removal
                   - Added <title>
                   - Renamed header > _header, footer > _footer
2019/05/17 (Simon) - Form action attribute uses relative path
2019/05/18 (Simon) - paymentdate input field now not required
</%doc>


<%page args="user=None"/>
<%inherit file="_base.mako"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/add.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
        <script src="/scripts/enable.js"></script>
        <title>PSYSC - Add Record</title>
    </head>
    <body>
        <header>
            <%include file="_header.mako" args="user=user, current='add'"/>
        </header>
        <div class="ui center aligned container">
            <h1 class="ui header title">Add Affiliation Record</h1>
            <div class="ui fluid raised blue left aligned container segment">
                <form method="post" action="./insert" id="add-form" class="ui form">
                    <div class="ui stackable grid">
                        <div class="sixteen wide blue column">
                            <h2 class="ui inverted header">Club Info</h2>
                        </div>
                        <div class="sixteen wide column">
                            <div class="required field">
                                <label>Club Name</label>
                                <input type="text" placeholder="Club Name" name="clubname" required>
                            </div>
                        </div>
                        <div class="eight wide column">
                            <div class="required field">
                                <label>School</label>
                                <input type="text" name="school" required placeholder="School Name">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Type</label>
                                <select class="ui fluid dropdown" name="type" id="type" required>
                                    <option value="1">Public</option>
                                    <option value="2">Private</option>
                                    <option value="3">State College/University</option>
                                </select>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Level/s</label>
                                <select class="ui fluid dropdown" name="level" id="level" required>
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
                                <input type="text" placeholder="Address" name="address" required>
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>City</label>
                                <input type="text" placeholder="City" name="city" required>
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>Province</label>
                                <input type="text" placeholder="Province" name="province" required>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Region</label>
                                <select class="ui fluid dropdown" name="region" id="region" required>
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
                                <input type="text" placeholder="Adviser Name" name="advisername" required>
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required field">
                                <label>Contact Number</label>
                                <input type="text" placeholder="Contact No." name="contact" required>
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required field">
                                <label>E-mail</label>
                                <input type="email" placeholder="Email Address" name="email" required>
                            </div>
                        </div>
                        <div class="ui horizontal hidden divider"></div>
                        <div class="sixteen wide blue column">
                            <h2 class="ui inverted header">Affiliation Info</h2>
                        </div>
                        <div class="three wide column">
                            <div class="required field">
                                <label>School Year</label>
                                <input type="number"  name="schoolyear" min="2007" max="2050" value = "2007" required>
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required grouped fields">
                                <label for="affiliated">Affiliated for school year?</label>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="affiliated" value="1" id="affiliated-yes" required>
                                        <label>Yes</label>
                                    </div>
                                </div>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="affiliated" value="0" id="affiliated-no" required>
                                        <label>No</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="five wide column">
                            <div class="required grouped fields">
                                <label>Submitted affiliation forms?</label>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                      <input type="radio" name="hasaffiliationforms" value="1" id="hasaffiliationforms-yes" required>
                                      <label>Yes</label>
                                    </div>
                                </div>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                      <input type="radio" name="hasaffiliationforms" value="0" id="hasaffiliationforms-no" required>
                                      <label>No</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="three wide column">
                            <div class="grouped fields">
                                <label>Status</label>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="status" value="N" id="status-n">
                                        <label>New</label>
                                    </div>
                                </div>
                                <div class="field">
                                    <div class="ui radio checkbox">
                                        <input type="radio" name="status" value="O" id="status-o">
                                        <label>Old</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="required field">
                                <label>Number of years paid</label>
                                <input type="number"  name="yearsaffiliated" min="1" value = "1" required>
                            </div>
                        </div>
                        <div class="six wide column">
                            <div class="required field">
                                <label>Number of club advisers</label>
                                <input type="number" name="sca" min="1" required>
                            </div>
                        </div>
                        <div class="six wide column">
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
                        <div class="three wide column">
                            <div class="field">
                                <label>Mode of Payment</label>
                                <input type="text" placeholder="Payment Mode" name="paymentmode">
                            </div>
                        </div>
                        <div class="five wide column">
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
                        <div class="four wide column">
                            <div class="field">
                                <label>Benefits</label>
                                <input type="text" placeholder="Benefits..." name="benefits">
                            </div>
                        </div>
                        <div class="four wide column">
                            <div class="field">
                                <label>Extra Remarks</label>
                                <input type="text" placeholder="Remarks..." name="remarks">
                            </div>
                        </div>
                        <div class="ui horizontal divider"></div>
                        <div class="sixteen wide column">
                            <button class='ui submit blue button' type="submit">Add Record</button>
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