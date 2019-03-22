# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file


from ._helpers import *
from .AddRecord import *

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
    # CherryPy method handling /add/
    def index(self):
        # returns Mako-rendered add page HTML
        return self.renderer.render("apply.mako")
    
    @cherrypy.expose
    # CherryPy method handling /apply/insert with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    def insert(self, hasrecord, clubid, region, level, type, school, clubname, address, city, province, advisername, contact, email, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        # string format for inserting record_data into SQL database
        # table structure is defined in db.sql
        add_application = (
            "INSERT INTO AffiliationApplicationsTable "
            "(appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode) "
            "VALUES (%(appID)s, %(hasRecord)s, %(clubID)s, %(dateCreated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s)"
        )
        
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        application_data = {
            'appID':                newID(),
            'hasRecord':            toInt(hasrecord),
            'clubID':               clubid,
            'dateCreated':          today(),
            
            'region':               toInt(region),
            'level':                toInt(level),
            'type':                 toInt(type),
            'school':               school,
            'clubName':             clubname,
            'address':              address,
            'city':                 city,
            'province':             province,
            'adviserName':          advisername,
            'contact':              contact,
            'email':                email,
            
            'schoolYear':           toInt(schoolyear),
            'yearsAffiliated':      toInt(yearsaffiliated),
            'SCA':                  toInt(sca),
            'SCM':                  toInt(scm),
            'paymentMode':          paymentmode,
            'paymentDate':          paymentdate,
            'paymentID':            paymentid,
            'paymentAmount':        toInt(paymentamount),
            'receiptNumber':        receiptnumber,
            'paymentSendMode':      paymentsendmode,
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
                "FROM AffiliationRecordsTable WHERE clubID = %(clubID)s"
            )
            cur.execute(club_query, {'clubID': clubid})
            if cur.rowcount == 1:
                # don't check record again (valid one is already fetched)
                skip_record_check = True
                record = cur.fetchone()
                application_data.update({
                    'clubID':       record[0],
                    'region':       record[1],
                    'level':        record[2],
                    'type':         record[3],
                    'school':       record[4],
                    'clubName':     record[5],
                    'address':      record[6],
                    'city':         record[7],
                    'province':     record[8],
                    'adviserName':  record[9],
                    'contact':      record[10],
                    'email':        record[11]
                })
            elif cur.rowcount == 0:
                errors.append(("Club with ID does not exist", "clubID", clubid))
                application_data['clubID'] = None
            else:
                errors.append(("More than one club with same ID", "clubID", clubid))
                application_data['clubID'] = None
        else:
            # check for preexisting record
            collision_query = 'SELECT clubID FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s'
            cur.execute(collision_query, {'school': school, 'clubName': clubname})
            if cur.rowcount > 0:
                errors.append(("Matching record already exists in the database", "school/club name", (school, clubname)))
        
        if application_data['clubID'] is not None:
            # check for preexisting affiliation (same clubID & overlapping school year range)
            collision2_query = 'SELECT affiliationID FROM AffiliationTable WHERE AffiliationRecordsTable_clubID = %(clubID)s AND (%(schoolYear)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated OR %(schoolYear)s-1+%(yearsAffiliated)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated)'
            print("coll: ", schoolyear, " ", yearsaffiliated)
            cur.execute(collision2_query, {'schoolYear': schoolyear, 'clubID': clubid, 'yearsAffiliated':yearsaffiliated})
            print(cur.rowcount)
            if cur.rowcount > 0:
                errors.append(("Matching affiliation already exists in the database", "clubID/school year/years affiliated", (clubid, schoolyear, yearsaffiliated)))
        
        # change validation method if record data is already known to be valid
        if skip_record_check:
            errors += self.validator.validate(application_data, [*self.validator.record_dict])
        else:
            errors += self.validator.validate(application_data)
        
        # display errors, if any
        if len(errors) > 0:
            cur.close() # close database cursor
            errortext = ""
            for e in errors:
                errortext += "["+str(e[0])+"] '"+str(e[1])+"': "+str(e[2])+"<br>"
            return self.renderer.render("dialog.mako", {
                'title': "Error!",
                'message': "Invalid inputs:<br>"+errortext,
                'linkaddr': "javascript:history.back();",
                'linktext': "&lt; Back"
            })
        cur.execute(add_application, application_data)  # insert application_data to database
        sqlcnx.commit()                                 # commit changes to database
        cur.close() # close database cursor
        return self.renderer.render("dialog.mako", {           # return insertion success HTML
            'title': "Sent an application.",
            'message': "",
        })
