# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users
#                    - Changed algorithm for generating application IDs
# 2019/02/27 (Simon) - Fixed non-conversion to string fro newID() calls
# 2019/03/29 (Simon) - "DBC" argument now indicates the database configuration settings
#                           instead of a DBConnection class
#                    - Database connection now handled using a with statement
# 2019/04/02 (Simon) - Changed field error handling, changed "back" URL
# 2019/04/05 (Simon) - insert() now uses unexposed _insert() method
#                    - Handle case of paymentDate being an empty string ""
# 2019/04/24 (Simon) - paymentDate coverted to string before displaying
#                    - New login credential generated upon adding a record
#                    - Backlink changed on successful insertion
# 2019/05/15 (Simon) - Added **kwargs to CherryPy-exposed methods to catch unexpected parameters w/o an error
#                    - Handles condition: add record for existing club+school, with non-colliding school year
# 2019/05/17 (Simon) - Update dateModified field row in AffiliationRecordsTable if a row is created in AffiliationTable
# 2019/05/24 (Simon) - Add "header" option for some render("dialog.mako") calls

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /add
class AddRecord(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBConnection(DBC)
        else:
            self.DBC = DBConnection("db.conf")
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
    def index(self, **kwargs):
        # returns Mako-rendered add page HTML
        return self.renderer.render("add.mako",
                                    {'user': getUserType(self.DBC)})

    # method handling the actual record insertion
    # every argument in the method (except for self) is defined in db.sql
    def _insert(self,
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
        with self.DBC as sqlcnx:
            # string format for inserting record_data into SQL database
            # table structure is defined in db.sql
            add_record = (
                "INSERT INTO AffiliationRecordsTable "
                "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
                "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)"
            )
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database
            date_today = today()
            id = newID(str(region) + str(level) + str(type) + str(school) +
                       str(clubname) + str(address) + str(city) +
                       str(province) + str(advisername) + str(contact) +
                       str(email),
                       length=8)  # generate new unique ID for record_data
            record_data = {
                'clubID': id,
                'dateUpdated': date_today,
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
                return self.renderer.render(
                    "dialog.mako", {
                        'title': "Error!",
                        'message':
                        "Invalid affiliation record data",
                        'linkaddr': "#back",
                        'linktext': "< Back",
                        'errors': errors,
                        'user': getUserType(self.DBC)
                    })
            # checking for preexisting affiliation from same club
            collision_query = "SELECT clubName FROM (AffiliationRecordsTable INNER JOIN AffiliationTable ON AffiliationRecordsTable.clubID = AffiliationTable.AffiliationRecordsTable_clubID) WHERE school = %(school)s AND clubName = %(clubName)s AND (%(schoolYear)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated OR %(schoolYear)s-1+%(yearsAffiliated)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated)"
            cur.execute(collision_query, {
                'school': school,
                'clubName': clubname,
                'schoolYear': schoolyear,
                'yearsAffiliated': yearsaffiliated
            })
            if cur.rowcount > 0:
                cur.close()  # close database cursor
                return self.renderer.render(
                    "dialog.mako", {
                        'title': "Error!",
                        'message':
                        "A matching record already exists in the database.",
                        'linkaddr': "#back",
                        'linktext': "< Back",
                        'user': getUserType(self.DBC)
                    })
            cur.fetchall()
            res = self.validate_affiliation(
                id, affiliated, status, hasaffiliationforms, benefits, remarks,
                schoolyear, yearsaffiliated, sca, scm, paymentmode,
                paymentdate, paymentid, paymentamount, receiptnumber,
                paymentsendmode)
            if len(res) > 0:
                cur.close()  # close database cursor
                return self.renderer.render(
                    "dialog.mako", {
                        'title': "Error!",
                        'message':
                        "Invalid affiliation record data",
                        'linkaddr': "#back",
                        'linktext': "< Back",
                        'errors': res,
                        'user': getUserType(self.DBC)
                    })
            # checking for preexisting affiliation from same club
            collision_query = "SELECT school, clubName FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s"
            cur.execute(collision_query, {
                'school': school,
                'clubName': clubname
            })
            # add new record only if school+clubname doesn't exist
            if cur.rowcount == 0:
                cur.execute(add_record,
                        record_data)  # insert record_data to database
            sqlcnx.commit()  # commit changes to database
            cur.close()  # close database cursor
            self.insert_affiliation(id, affiliated, status,
                                    hasaffiliationforms, benefits, remarks,
                                    schoolyear, yearsaffiliated, sca, scm,
                                    paymentmode, paymentdate, paymentid,
                                    paymentamount, receiptnumber,
                                    paymentsendmode)
            createCredentials(id, id, 0, self.DBC)  # create club credentials
            return self.renderer.render(
                "dialog.mako",
                {  # return insertion success HTML
                    'title': "Affiliation record added.",
                    'linkaddr': "/view/" + str(id),
                    'linktext': "< Go to record",
                    'linkaddr2': "/add",
                    'linktext2': "< Add another record",
                    'user': getUserType(self.DBC)
                })
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'header': False
            })

    @cherrypy.expose
    @accessible_by("admin")
    # CherryPy method handling /add/insert with incoming POST/GET data
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
               paymentsendmode=None,
               **kwargs):
        return self._insert(region, level, type, school, clubname, address,
                            city, province, advisername, contact, email,
                            affiliated, status, hasaffiliationforms, benefits,
                            remarks, schoolyear, yearsaffiliated, sca, scm,
                            paymentmode, paymentdate, paymentid, paymentamount,
                            receiptnumber, paymentsendmode)

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
            'paymentID': paymentid,
            'paymentAmount': toInt(paymentamount),
            'receiptNumber': receiptnumber,
            'paymentSendMode': paymentsendmode,
            'AffiliationRecordsTable_clubID': clubid
        }
        if paymentdate is not None:
            if len(str(paymentdate)) > 0:
                affiliation_data["paymentDate"] = str(paymentdate)
            else:
                affiliation_data["paymentDate"] = None
        else:
            affiliation_data["paymentDate"] = None
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
        with self.DBC as sqlcnx:
            date_today = today()
            # string format for inserting affiliation_data into SQL database
            # table structure is defined in db.sql
            add_affiliation = (
                "INSERT INTO AffiliationTable "
                "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
                "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)"
            )
            affiliation_data = {
                'affiliationID':
                newID(
                    str(affiliated) + str(status) + str(hasaffiliationforms) +
                    str(benefits) + str(remarks) + str(schoolyear) +
                    str(yearsaffiliated) + str(sca) + str(scm) +
                    str(paymentmode) + str(paymentdate) + str(paymentid) +
                    str(paymentamount) + str(receiptnumber) +
                    str(paymentsendmode) + str(clubid)
                ),  # generate new unique ID for affiliation_data
                'affiliated':
                toInt(affiliated),
                'status':
                status,
                'hasAffiliationForms':
                toInt(hasaffiliationforms),
                'benefits':
                benefits,
                'remarks':
                remarks,
                'schoolYear':
                toInt(schoolyear),
                'yearsAffiliated':
                toInt(yearsaffiliated),
                'SCA':
                toInt(sca),
                'SCM':
                toInt(scm),
                'paymentMode':
                paymentmode,
                'paymentDate':
                paymentdate,
                'paymentID':
                paymentid,
                'paymentAmount':
                toInt(paymentamount),
                'receiptNumber':
                receiptnumber,
                'paymentSendMode':
                paymentsendmode,
                'AffiliationRecordsTable_clubID':
                clubid
            }
            if paymentdate is not None:
                if len(str(paymentdate)) > 0:
                    affiliation_data["paymentDate"] = str(paymentdate)
                else:
                    affiliation_data["paymentDate"] = None
            else:
                affiliation_data["paymentDate"] = None
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database
            cur.execute(
                add_affiliation,
                affiliation_data)  # insert affiliation_data to database
            cur.execute("UPDATE AffiliationRecordsTable SET dateUpdated = %(dateUpdated)s WHERE clubID = %(clubID)s",{
                "dateUpdated": date_today,
                "clubID": clubid
            })
            sqlcnx.commit()  # commit changes to database
            cur.close()  # close database cursor
