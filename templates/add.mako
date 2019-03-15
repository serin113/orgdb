<%doc>
Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/06 (Simon) - Initial working code and documentation
2019/02/13 (Simon) - Added Mako templating
2019/02/14 (Simon) - renamed to add.mako
2019/02/15 (Simon) - added <section> tags
</%doc>


<%doc>
Mako variables:
    none
</%doc>


<html>
    <head>
       <link rel="stylesheet" href="/styles/add.css"/>
       <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
       <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
       <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/fomantic-ui/2.7.2/semantic.min.css">
       <script src="https://cdnjs.cloudflare.com/ajax/libs/fomantic-ui/2.7.2/semantic.min.js"></script>

    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">Add Affiliation Record</h1>

            <form method="post" action="insert" id="add-form"><br>
                <div class="ui placeholder segment">
                    <div class="ui two column very relaxed stackable grid">
                        <div class="column">
                      <div class="ui input">
                                        <input type="text" placeholder="Club Name" name="clubname" required/ placeholder="Club Name">
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="text" name="school" required/ placeholder="School Name">
                                      </div>
                                      <br><br>

                                      <div class="ui selection dropdown">
                                        <input type="hidden" name="region" id="region required">
                                        <i class="dropdown icon"></i>
                                        <div class="default text">Region</div>
                                        <div class="menu">
                                          <script>
                                              $('.ui.dropdown')
                                                .dropdown();
                                          </script>
                                          <div class="item" data-value="1">I (Ilocos)</div>
                                          <div class="item" data-value="2">II (Cagayan Valley)</div>
                                          <div class="item" data-value="3">III (Central Luzon)</div>
                                          <div class="item" data-value="4">IV-A (CALABARZON)</div>
                                          <div class="item" data-value="5">V (Bicol)</div>
                                          <div class="item" data-value="6">VI (Western Visayas)</div>
                                          <div class="item" data-value="7">VII (Central Visayas)</div>
                                          <div class="item" data-value="8">VIII (Eastern Visayas)</div>
                                          <div class="item" data-value="9">IX (Zamboanga Peninsula)</div>
                                          <div class="item" data-value="10">X (Northern Mindanao)</div>
                                          <div class="item" data-value="11">XI (Davao)</div>
                                          <div class="item" data-value="12">XII (SOCCSKSARGEN)</div>
                                          <div class="item" data-value="13">XIV (NCR)</div>
                                          <div class="item" data-value="14">XV (CAR)</div>
                                          <div class="item" data-value="15">XVI (ARMM)</div>
                                          <div class="item" data-value="16">XII (CARAGA)</div>
                                          <div class="item" data-value="17">XVII (MIMAROPA)</div>
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
                                      
                                      <div class="ui form">
                                          <label>Type</label>
                                          <div class="field">
                                            <div class="ui radio checkbox">
                                              <input type="radio" name="type" value="1" id="type-public"  required>
                                              <label for="type-public">Public</label>
                                            </div>
                                          </div>
                                          <div class="field">
                                            <div class="ui radio checkbox">
                                              <input type="radio" name="type" value="2" id="type-private" required>
                                              <label for="type-private">Private</label>
                                            </div>
                                          </div>
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="text" placeholder="Address" name="address" required>
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
                      <label>School Year: </label> &nbsp&nbsp
                                      <div class="ui input">
                                        <input type="number"  name="schoolyear" min="2007" max="3050" value = "2007" required style="width: 100px;">
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
                                              <input type="radio" name="status" value="O" id="status-o" required>
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

                                      <label>Number of years paid: </label> &nbsp&nbsp
                                      <div class="ui input">
                                        <input type="number"  name="yearsaffiliated" min="1" value = "1" required style="width: 100px;">
                                      </div><br><br>

                                      <label>Number of club advisers: </label> &nbsp&nbsp
                                      <div class="ui input">
                                        <input type="number" name="sca" min="1"required style="width: 100px;">
                                      </div><br><br>

                                      <label>Number of club members: </label> &nbsp&nbsp
                                      <div class="ui input">
                                        <input type="number"  name="scm" min="1" required style="width: 100px;">
                                      </div><br><br>

                                      <label>Payment Amount: </label> &nbsp&nbsp
                                      <div class="ui input">
                                        <input type="number"  name="paymentamount" min="0" style="width: 100px;">
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="text" placeholder="Payment Mode" name="paymentmode" required>
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="date" name="paymentdate" required>
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="text" placeholder="Payment ID" name="paymentid" required>
                                      </div><br><br>

                                      

                                      <div class="ui input">
                                        <input type="text" placeholder="Receipt #" name="receiptnumber" required>
                                      </div><br><br>

                                      <div class="ui input">
                                        <input type="text" placeholder="Payment Send Mode" name="paymentsendmode" required>
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
                <div class="ui vertical divider">
                    *
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