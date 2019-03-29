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
</%doc>


<%page args="user=None"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/add.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='add'"/>
        </header>
        <section class="ui container">
            <h1 class="ui header center title">Add Affiliation Record</h1>
            <form method="post" action="insert" id="add-form"><br>
                <div class="ui placeholder segment">
                    <div class="ui two column very relaxed stackable grid">
                        <div class="column">
                          <div class="ui input">
                            <input type="text" placeholder="Club Name" name="clubname" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" name="school" required placeholder="School Name">
                          </div>
                          <br><br>

                          <div class="ui selection dropdown">
                            <input type="hidden" name="region" id="region" required>
                            <i class="dropdown icon"></i>
                            <div class="default text">Region</div>
                            <div class="menu">
                              <script>
                                  $('.ui.dropdown')
                                    .dropdown();
                              </script>
                              <div class="item" data-value="1">1 (Ilocos)</div>
                              <div class="item" data-value="2">2 (Cagayan Valley)</div>
                              <div class="item" data-value="3">3 (Central Luzon)</div>
                              <div class="item" data-value="4">4A (CALABARZON)</div>
                              <div class="item" data-value="5">5 (Bicol)</div>
                              <div class="item" data-value="6">6 (Western Visayas)</div>
                              <div class="item" data-value="7">7 (Central Visayas)</div>
                              <div class="item" data-value="8">8 (Eastern Visayas)</div>
                              <div class="item" data-value="9">9 (Zamboanga Peninsula)</div>
                              <div class="item" data-value="10">10 (Northern Mindanao)</div>
                              <div class="item" data-value="11">11 (Davao)</div>
                              <div class="item" data-value="12">12 (SOCCSKSARGEN)</div>
                              <div class="item" data-value="13">13 (NCR)</div>
                              <div class="item" data-value="14">14 (CAR)</div>
                              <div class="item" data-value="15">15 (ARMM)</div>
                              <div class="item" data-value="16">16 (CARAGA)</div>
                              <div class="item" data-value="17">17 (MIMAROPA)</div>
                            </div>
                          </div><br><br>
                          
                          <div class="ui selection dropdown">
                            <input type="hidden" name="level" id="level" required>
                            <i class="dropdown icon"></i>
                            <div class="default text">Level</div>
                            <div class="menu">
                              <script>
                                  $('.ui.dropdown')
                                    .dropdown();
                              </script>
                              <div class="item" data-value="1">Elementary</div>
                              <div class="item" data-value="2">High School</div>
                              <div class="item" data-value="3">Elementary & High School</div>
                              <div class="item" data-value="4">College</div>
                            </div>
                          </div><br><br>
                          
                          <div class="ui selection dropdown">
                            <input type="hidden" name="type" id="type" required>
                            <i class="dropdown icon"></i>
                            <div class="default text">Type</div>
                            <div class="menu">
                              <script>
                                  $('.ui.dropdown')
                                    .dropdown();
                              </script>
                              <div class="item" data-value="1">Public</div>
                              <div class="item" data-value="2">Private</div>
                              <div class="item" data-value="3">State College/University</div>
                            </div>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Address" name="address" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="City" name="city" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Province" name="province" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Adviser Name" name="advisername" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Contact No." name="contact" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Email Address" name="email" required>
                          </div><br><br>
                        </div>
                        <div class="column">
                          <label>School Year: </label> &nbsp;&nbsp;
                          <div class="ui input">
                            <input type="number"  name="schoolyear" min="2007" max="2050" value = "2007" required style="width: 100px;">
                          </div><br><br>
                          

                          <div class="ui form">
                              <label>Affiliated for the given school year?</label>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="affiliated" value="1" id="affiliated-yes" required>
                                  <label for="affiliated-yes">Yes</label>
                                </div>
                              </div>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="affiliated" value="0" id="affiliated-no" required>
                                  <label for="affiliated-no">No</label>
                                </div>
                              </div>
                          </div><br>

                          <div class="ui form">
                              <label>Status</label>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="status" value="N" id="status-n">
                                  <label for="status-N">N</label>
                                </div>
                              </div>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="status" value="O" id="status-o">
                                  <label for="affiliated-no">O</label>
                                </div>
                              </div>
                          </div><br><br>

                          <div class="ui form">
                              <label>Submitted affiliation forms?</label>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="hasaffiliationforms" value="1" id="hasaffiliationforms-yes" required>
                                  <label for="hasaffiliationforms-yes">Yes</label>
                                </div>
                              </div>
                              <div class="field">
                                <div class="ui radio checkbox">
                                  <input type="radio" name="hasaffiliationforms" value="0" id="hasaffiliationforms-no" required>
                                  <label for="hasaffiliationforms-no">No</label>
                                </div>
                              </div>
                          </div><br><br>

                          <label>Number of years paid: </label> &nbsp;&nbsp;
                          <div class="ui input">
                            <input type="number"  name="yearsaffiliated" min="1" value = "1" required style="width: 100px;">
                          </div><br><br>

                          <label>Number of club advisers: </label> &nbsp;&nbsp;
                          <div class="ui input">
                            <input type="number" name="sca" min="1" required style="width: 100px;">
                          </div><br><br>

                          <label>Number of club members: </label> &nbsp;&nbsp;
                          <div class="ui input">
                            <input type="number"  name="scm" min="1" required style="width: 100px;">
                          </div><br><br>

                          <label>Payment Amount: </label> &nbsp;&nbsp;
                          <div class="ui input">
                            <input type="number"  name="paymentamount" min="0" style="width: 100px;">
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Payment Mode" name="paymentmode">
                          </div><br><br>

                          <div class="ui input">
                            <input type="date" name="paymentdate" required>
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Payment ID" name="paymentid">
                          </div><br><br>

                          

                          <div class="ui input">
                            <input type="text" placeholder="Receipt #" name="receiptnumber">
                          </div><br><br>

                          <div class="ui input">
                            <input type="text" placeholder="Payment Send Mode" name="paymentsendmode">
                          </div><br><br>

                          <div class="ui form">
                              <div class="ui input">
                                  <textarea placeholder="Benefits..." style="width: 300px;" name="benefits"></textarea>
                              </div>
                          </div><br><br>

                          <div class="ui form">
                              <div class="ui input">
                                  <textarea placeholder="Remarks..." style="width: 300px;" name="remarks"></textarea>
                              </div>
                          </div><br><br>
                        </div>
                      </div>
                </div>
                <button class='ui primary button' type="submit">INSERT</button>
            </form>
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>