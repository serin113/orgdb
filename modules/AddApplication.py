# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users
#                    - Changed algorithm for generating application IDs

from ._helpers import *
from .AddRecord import *
from .Login import *


# class used by CherryPy for handling /apply
class AddApplication(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        if Validator is not None:
            self.validator = Validator
        else:
            self.validator = InputValidator()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()

    @cherrypy.expose
    @accessible_by(["default", "club"])
    # CherryPy method handling /add/
    def index(self):
        # returns Mako-rendered add page HTML
        return self.renderer.render("apply.mako",
                                    {'user': getUserType(self.DBC)})

    @cherrypy.expose
    @accessible_by(["default", "club"])
    # CherryPy method handling /apply/insert with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    def insert(self,
               hasrecord=None,
               clubid=None,
               region=None,
               level=None,
               type=None,
               school=None,
               clubname=None,
               address=None,
               city=None,
               province=None,
               advisername=None,
               contact=None,
               email=None,
               schoolyear=None,
               yearsaffiliated=None,
               sca=None,
               scm=None,
               paymentmode=None,
               paymentdate=None,
               paymentid=None,
               paymentamount=None,
               receiptnumber=None,
               paymentsendmode=None):
        # string format for inserting record_data into SQL database
        # table structure is defined in db.sql
        add_application = (
            "INSERT INTO AffiliationApplicationsTable "
            "(appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode) "
            "VALUES (%(appID)s, %(hasRecord)s, %(clubID)s, %(dateCreated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s)"
        )

        sqlcnx = self.DBC.connect()  # connect to SQL server
        cur = sqlcnx.cursor(
            buffered=True)  # create an SQL cursor to the database
        date_today = today()
        application_data = {
            'hasRecord': toInt(hasrecord),
            'clubID': clubid,
            'dateCreated': date_today,
            'region': toInt(region),
            'level': toInt(level),
            'type': toInt(type),
            'school': school,
            'clubName': clubname,
            'address': address,
            'city': city,
            'province': province,
            'adviserName': advisername,
            'contact': contact,
            'email': email,
            'schoolYear': toInt(schoolyear),
            'yearsAffiliated': toInt(yearsaffiliated),
            'SCA': toInt(sca),
            'SCM': toInt(scm),
            'paymentMode': paymentmode,
            'paymentDate': paymentdate,
            'paymentID': paymentid,
            'paymentAmount': toInt(paymentamount),
            'receiptNumber': receiptnumber,
            'paymentSendMode': paymentsendmode,
        }
        # input validation
        self.validator.setLimits("application")

        # checking for preexisting record
        skip_record_check = False
        errors = []
        # if user indicates "record exists"
        if toInt(hasrecord) is 1:
            # tl;dr: check if clubID is actually valid, and use it
            club_query = (
                "SELECT clubID, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                "FROM AffiliationRecordsTable WHERE clubID = %(clubID)s")
            cur.execute(club_query, {'clubID': clubid})
            if cur.rowcount == 1:
                # don't check record again (valid one is already fetched)
                skip_record_check = True
                record = cur.fetchone()
                application_data.update({
                    'clubID': record[0],
                    'region': record[1],
                    'level': record[2],
                    'type': record[3],
                    'school': record[4],
                    'clubName': record[5],
                    'address': record[6],
                    'city': record[7],
                    'province': record[8],
                    'adviserName': record[9],
                    'contact': record[10],
                    'email': record[11]
                })
            elif cur.rowcount == 0:
                errors.append(("Invalid club ID", "clubID", clubid))
                application_data['clubID'] = None
            else:
                errors.append(("More than one club with same ID", "clubID",
                               clubid))
                application_data['clubID'] = None
        else:
            # check for preexisting record
            collision_query = 'SELECT clubID FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s'
            cur.execute(collision_query, {
                'school': school,
                'clubName': clubname
            })
            if cur.rowcount > 0:
                errors.append(
                    ("Matching record already exists in the database",
                     "school/club name", (school, clubname)))

        if application_data['clubID'] is not None:
            # check for preexisting affiliation (same clubID & overlapping school year range)
            collision2_query = 'SELECT affiliationID FROM AffiliationTable WHERE AffiliationRecordsTable_clubID = %(clubID)s AND (%(schoolYear)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated OR %(schoolYear)s-1+%(yearsAffiliated)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated)'
            cur.execute(
                collision2_query, {
                    'schoolYear': schoolyear,
                    'clubID': clubid,
                    'yearsAffiliated': yearsaffiliated
                })
            if cur.rowcount > 0:
                errors.append(
                    ("Matching affiliation already exists in the database",
                     "clubID/school year/years affiliated",
                     (clubid, schoolyear, yearsaffiliated)))
                     
            application_data['appID'] = newID(
                    str(application_data['hasRecord']) +
                    str(application_data['clubID']) +
                    str(application_data['dateCreated']) +
                    str(application_data['region']) +
                    str(application_data['level']) +
                    str(application_data['type']) +
                    str(application_data['school']) +
                    str(application_data['clubName']) +
                    str(application_data['address']) +
                    str(application_data['city']) +
                    str(application_data['province']) +
                    str(application_data['adviserName']) +
                    str(application_data['contact']) +
                    str(application_data['email']) +
                    str(application_data['schoolYear']) +
                    str(application_data['yearsAffiliated']) +
                    str(application_data['SCA']) +
                    str(application_data['SCM']) +
                    str(application_data['paymentMode']) +
                    str(application_data['paymentDate']) +
                    str(application_data['paymentID']) +
                    str(application_data['paymentAmount']) +
                    str(application_data['receiptNumber']) +
                    str(application_data['paymentSendMode'])
                )

            # change validation method if record data is already known to be valid
            if skip_record_check:
                errors += self.validator.validate(
                    application_data, [*self.validator.record_dict])
            else:
                errors += self.validator.validate(application_data)

        # display errors, if any
        if len(errors) > 0:
            cur.close()  # close database cursor
            errortext = ""
            for e in errors:
                errortext += "[" + str(e[0]) + "] '" + str(e[1]) + "': " + str(
                    e[2]) + "<br>"
            return self.renderer.render(
                "dialog.mako", {
                    'title': "Error",
                    'message': errortext,
                    'linkaddr': "javascript:history.back();",
                    'linktext': "&lt; Back",
                    'user': getUserType(self.DBC)
                })
        cur.execute(add_application,
                    application_data)  # insert application_data to database
        sqlcnx.commit()  # commit changes to database
        cur.close()  # close database cursor
        return self.renderer.render(
            "dialog.mako",
            {  # return insertion success HTML
                'title': "Sent an application.",
                'message': "",
                'user': getUserType(self.DBC)
            })
