<%doc>
Created in 2019-03-06 for PSYSC as part of a system for managing science club affiliations.

Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

Code History:
2019/03/06 (Simon) - Initial working code and documentation
</%doc>


<%doc>
Mako variables:
    none
</%doc>


<html>
    <head>
        <link rel="stylesheet" href="/styles/apply.css"/>
    </head>
    <body>
        <header>
            <%include file="header.mako"/>
        </header>
        <section>
            <h1 class="center title">Application Form</h1>
            <hr>
            <form method="post" action="insert" id="apply-form">
                has existing record?<br><input type="radio" name="hasrecord" value="1" id="hasrecord-yes" required><label for="hasrecord-yes">Yes</label> <input type="radio" name="hasrecord" value="0" id="hasrecord-no" checked required><label for="hasrecord-no">No</label><br><br>
                <hr>
                (this section only required if there's an existing record)<br><br>
                club ID<br><input type="text" name="clubid" value=""/><br><br>
                <hr>
                (this section only required if there's no existing record)<br><br>
                club name<br><input type="text" name="clubname"/><br><br>
                school<br><input type="text" name="school"/><br><br>
                region<br>
                <select name="region" id="region">
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
                level<br><select name="level" id="level">
                    <option value="1" checked>Elementary</>
                    <option value="2">High School</>
                    <option value="3">Elementary & High School</>
                    <option value="4">College</>
                </select><br><br>
                type<br><input type="radio" name="type" value="1" id="type-public" checked><label for="type-public">Public</label> <input type="radio" name="type" value="2" id="type-private"><label for="type-private">Private</label><br><br>
                address<br><input type="text" name="address"/><br><br>
                city<br><input type="text" name="city"/><br><br>
                province<br><input type="text" name="province"/><br><br>
                adviser name/s<br><input type="text" name="advisername"/><br><br>
                contact number<br><input type="text" name="contact"/><br><br>
                email<br><input type="email" name="email" /><br><br>
                <hr>
                schoolyear<br><input type="number" name="schoolyear" min="2007" max="2050" required/><br><br>
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