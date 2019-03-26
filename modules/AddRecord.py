# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /add
class AddRecord(object):
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
    @accessible_by("admin")
    # CherryPy method handling /add/
    def index(self):
        # returns Mako-rendered add page HTML
        return self.renderer.render("add.mako",
                                    {'user': getUserType(self.DBC)})

    @cherrypy.expose
    @accessible_by("admin")
    # CherryPy method handling /add/insert with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    def insert(self,
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
               affiliated=None,
               status=None,
               hasaffiliationforms=None,
               benefits=None,
               remarks=None,
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
        add_record = (
            "INSERT INTO AffiliationRecordsTable "
            "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
            "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)"
        )

        sqlcnx = self.DBC.connect()  # connect to SQL server
        cur = sqlcnx.cursor(
            buffered=True)  # create an SQL cursor to the database
        id = newID()  # generate new unique ID for record_data
        record_data = {
            'clubID': id,
            'dateUpdated': today(),
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
            'email': email
        }

        # input validation
        self.validator.setLimits("record")
        errors = self.validator.validate(record_data)
        # display errors, if any
        if len(errors) > 0:
            cur.close()  # close database cursor
            errortext = ""
            for e in errors:
                errortext += "[" + str(e[0]) + "] '" + str(e[1]) + "': " + str(
                    e[2]) + "<br>"
            return self.renderer.render(
                "dialog.mako", {
                    'title': "Error!",
                    'message':
                    "Invalid affiliation record data:<br>" + errortext,
                    'linkaddr': "javascript:history.back();",
                    'linktext': "&gt; Back",
                    'user': getUserType(self.DBC)
                })
        # checking for preexisting record
        collision_query = "SELECT school, clubName, schoolYear FROM (AffiliationRecordsTable INNER JOIN AffiliationTable ON AffiliationRecordsTable.clubID = AffiliationTable.AffiliationRecordsTable_clubID) WHERE school = %(school)s AND clubName = %(clubName)s AND schoolYear = %(schoolYear)s"
        cur.execute(collision_query, {
            'school': school,
            'clubName': clubname,
            'schoolYear': schoolyear
        })
        if cur.rowcount > 0:
            cur.close()  # close database cursor
            return self.renderer.render(
                "dialog.mako", {
                    'title': "Error!",
                    'message':
                    "A matching record already exists in the database.",
                    'linkaddr': "javascript:history.back();",
                    'linktext': "&gt; Back",
                    'user': getUserType(self.DBC)
                })
        res = self.validate_affiliation(
            id, affiliated, status, hasaffiliationforms, benefits, remarks,
            schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate,
            paymentid, paymentamount, receiptnumber, paymentsendmode)
        if len(res) > 0:
            cur.close()  # close database cursor
            errortext = ""
            for e in res:
                errortext += "[" + str(e[0]) + "] '" + str(e[1]) + "': " + str(
                    e[2]) + "<br>"
            return self.renderer.render(
                "dialog.mako", {
                    'title': "Error!",
                    'message':
                    "Invalid affiliation record data:<br>" + errortext,
                    'linkaddr': "javascript:history.back();",
                    'linktext': "&gt; Back",
                    'user': getUserType(self.DBC)
                })
        cur.execute(add_record, record_data)  # insert record_data to database
        sqlcnx.commit()  # commit changes to database
        cur.close()  # close database cursor
        self.insert_affiliation(id, affiliated, status, hasaffiliationforms,
                                benefits, remarks, schoolyear, yearsaffiliated,
                                sca, scm, paymentmode, paymentdate, paymentid,
                                paymentamount, receiptnumber, paymentsendmode)
        return self.renderer.render(
            "dialog.mako",
            {  # return insertion success HTML
                'title': "Affiliation record added.",
                'linkaddr': "/add",
                'linktext': "Add another record",
                'user': getUserType(self.DBC)
            })

    def validate_affiliation(self,
                             clubid=None,
                             affiliated=None,
                             status=None,
                             hasaffiliationforms=None,
                             benefits=None,
                             remarks=None,
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
        affiliation_data = {
            'affiliationID':
            newID(),  # generate new unique ID for affiliation_data
            'affiliated': toInt(affiliated),
            'status': status,
            'hasAffiliationForms': toInt(hasaffiliationforms),
            'benefits': benefits,
            'remarks': remarks,
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
            'AffiliationRecordsTable_clubID': clubid
        }
        # input validation
        self.validator.setLimits("affiliation")
        errors = self.validator.validate(affiliation_data)
        return errors

    def insert_affiliation(self,
                           clubid=None,
                           affiliated=None,
                           status=None,
                           hasaffiliationforms=None,
                           benefits=None,
                           remarks=None,
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
        # string format for inserting affiliation_data into SQL database
        # table structure is defined in db.sql
        add_affiliation = (
            "INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)"
        )
        affiliation_data = {
            'affiliationID':
            newID(),  # generate new unique ID for affiliation_data
            'affiliated': toInt(affiliated),
            'status': status,
            'hasAffiliationForms': toInt(hasaffiliationforms),
            'benefits': benefits,
            'remarks': remarks,
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
            'AffiliationRecordsTable_clubID': clubid
        }
        sqlcnx = self.DBC.connect()  # connect to SQL server
        cur = sqlcnx.cursor(
            buffered=True)  # create an SQL cursor to the database
        cur.execute(add_affiliation,
                    affiliation_data)  # insert affiliation_data to database
        sqlcnx.commit()  # commit changes to database
        cur.close()  # close database cursor
