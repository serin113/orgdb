<%doc>
Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/02/06 - Initial working code and documentation
2019/02/13 - Added Mako templating
2019/02/14 - renamed to add.mako
2019/02/15 - added <section> tags
</%doc>


<%doc>
Mako variables:
    none
</%doc>


<html>
    <head>
        <link rel="stylesheet" href="/styles/add.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">Add Affiliation Record</h1>
            <hr>
            <form method="post" action="insert" id="add-form">
                club name<br><input type="text" name="clubname" required/><br><br>
                school<br><input type="text" name="school" required/><br><br>
                region<br>
                <select name="region" id="region" required>
                    <option value="1" checked>I (Ilocos)</option>
                    <option value="2">II (Cagayan Valley)</option>
                    <option value="3">III (Central Luzon)</option>
                    <option value="4">IV-A (CALABARZON)</option>
                    <option value="5">V (Bicol)</option>
                    <option value="6">VI (Western Visayas)</option>
                    <option value="7">VII (Central Visayas)</option>
                    <option value="8">VIII (Eastern Visayas)</option>
                    <option value="9">IX (Zamboanga Peninsula)</option>
                    <option value="10">X (Northern Mindanao)</option>
                    <option value="11">XI (Davao)</option>
                    <option value="12">XII (SOCCSKSARGEN)</option>
                    <option value="13">XIV (NCR)</option>
                    <option value="14">XV (CAR)</option>
                    <option value="15">XVI (ARMM)</option>
                    <option value="16">XII (CARAGA)</option>
                    <option value="17">XVII (MIMAROPA)</option>
                </select><br><br>
                level<br><select name="level" id="level" required>
                    <option value="1" checked>Elementary</>
                    <option value="2">High School</>
                    <option value="3">Elementary & High School</>
                    <option value="4">College</>
                </select><br><br>
                type<br><input type="radio" name="type" value="1" id="type-public" checked required><label for="type-public">Public</label> <input type="radio" name="type" value="2" id="type-private" required><label for="type-private">Private</label><br><br>
                address<br><input type="text" name="address" required/><br><br>
                city<br><input type="text" name="city" required/><br><br>
                province<br><input type="text" name="province" required/><br><br>
                adviser name/s<br><input type="text" name="advisername" required/><br><br>
                contact number<br><input type="text" name="contact" required/><br><br>
                email<br><input type="email" name="email" /><br><br>
                <hr>
                schoolyear<br><input type="number" name="schoolyear" min="2007" max="2050" required/><br><br>
                affiliated for the given school year?<br><input type="radio" name="affiliated" value="1" id="affiliated-yes" checked required><label for="affiliated-yes">yes</label> <input type="radio" name="affiliated" value="0" id="affiliated-no" required><label for="affiliated-no">no</label><br><br>
                status<br><input type="text" name="status" /><br><br>
                submitted affiliation forms?<br><input type="radio" name="hasaffiliationforms" value="1" id="hasaffiliationforms-yes" checked required><label for="hasaffiliationforms-yes">yes</label> <input type="radio" name="hasaffiliationforms" value="0" id="hasaffiliationforms-no" required><label for="hasaffiliationforms-no">no</label><br><br>
                benefits<br><input type="text" name="benefits" /><br><br>
                remarks<br><input type="text" name="remarks" /><br><br>
                number of years paid<br><input type="number" name="yearsaffiliated" min="1" value="1" required/><br><br>
                number of club advisers<br><input type="number" name="sca" min="1" required/><br><br>
                number of club members<br><input type="number" name="scm" min="1" required/><br><br>
                payment mode<br><input type="text" name="paymentmode" /><br><br>
                payment date<br><input type="date" name="paymentdate" /><br><br>
                payment id<br><input type="text" name="paymentid" /><br><br>
                payment amount<br><input type="number" name="paymentamount" min="0"><br><br>
                receipt number<br><input type="text" name="receiptnumber" /><br><br>
                payment sendmode<br><input type="text" name="paymentsendmode" /><br><br>
                <hr>
                <button type="submit">insert</button>
            </form>
        </section>
        <footer>
            <%include file="footer.mako"/>
        </footer>
    </body>
</html>