<%doc>
Created in 2019-03-06 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/06 (Simon) - Initial working code and documentation
2019/03/23 (Simon) - Changed region numbers from Roman to Arabic
2019/03/26 (Simon) - Changed page arguments, updated UI
2019/03/29 (Simon) - Added <meta name="viewport"> to scale properly in mobile screens
</%doc>


<%page args="user=None"/>


<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="/styles/apply.css"/>
        <link rel="stylesheet" type="text/css" href="/styles/semantic.min.css">
        <script src="/scripts/jquery-3.3.1.min.js"></script>
        <script src="/scripts/semantic.min.js"></script>
    </head>
    <body>
        <header>
            <%include file="header.mako" args="user=user, current='apply'"/>
        </header>
        <section class="ui container">
            <h1 class="center title">Application Form</h1>
            <hr>
            <form method="post" action="insert" id="apply-form">
                
                <div class="ui form">
                    <label>Has existing record?</label>
                    <div class="field">
                      <div class="ui radio checkbox">
                        <input type="radio" name="hasrecord" value="1" id="hasrecord-yes" required>
                        <label for="hasrecord-yes">Yes</label>
                      </div>
                    </div>
                    <div class="field">
                      <div class="ui radio checkbox">
                        <input type="radio" name="hasrecord" value="0" id="hasrecord-no" required>
                        <label for="hasrecord-no">No</label>
                      </div>
                    </div>
                </div><br>

                <hr>
                (this section only required if there's an existing record)<br>
                <div class="ui input">
                    <input type="text" name="clubid" placeholder="Club ID">
                </div>
                <hr>
                
                (this section only required if there's no existing record)<br><br>
                <div class="ui input">
                <input type="text" placeholder="Club Name" name="clubname">
              </div><br><br>

              <div class="ui input">
                <input type="text" name="school" placeholder="School Name">
              </div>
              <br><br>

              <div class="ui selection dropdown">
                <input type="hidden" name="region" id="region" value="1">
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
                <input type="hidden" name="level" id="level" value="1">
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
              
              <div class="ui form">
                  <label>Type</label>
                  <div class="field">
                    <div class="ui radio checkbox">
                      <input type="radio" name="type" value="1" id="type-public" checked>
                      <label for="type-public">Public</label>
                    </div>
                  </div>
                  <div class="field">
                    <div class="ui radio checkbox">
                      <input type="radio" name="type" value="2" id="type-private">
                      <label for="type-private">Private</label>
                    </div>
                  </div>
                  <div class="field">
                    <div class="ui radio checkbox">
                      <input type="radio" name="type" value="3" id="type-scu">
                      <label for="type-private">State College/University</label>
                    </div>
                  </div>
              </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="Address" name="address">
                </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="City" name="city">
                </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="Province" name="province">
                </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="Adviser Name" name="advisername">
                </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="Contact No." name="contact">
                </div><br><br>

                <div class="ui input">
                    <input type="text" placeholder="Email Address" name="email">
                </div><br><br>

                <hr>
                <label>School Year: </label> &nbsp;&nbsp;
                <div class="ui input">
                    <input type="number"  name="schoolyear" min="2007" max="3050" value = "2007" required style="width: 100px;">
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
                <hr>
                <button class="ui primary button" type="submit">INSERT</button>
            </form>
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>