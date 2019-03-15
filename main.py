# Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/02/06 (Simon) - Initial working code and documentation
# 2019/02/08 (Simon) - Updated CherryPy config, added getContent()
# 2019/02/13 (Simon) - Added Mako for rendering dynamic content, renamed getContent to renderContent
# 2019/02/19 (Simon) - Renamed class AffiliationDB to Root
#                    - Removed classes AffiliationRecord and Affiliation: all handled by class ViewRecord
#                        - URL scheme changed from /view/r/<r>/a/<a> to /view/<r>/<a>
# 2019/02/20 (Simon) - Updated documentation
#                    - Fixed templatelookup for caching locally
#                    - Added class DBConnection for handling a single persistent SQL database connection
#                    - Added atexit handler to disconnect from SQL database
#                    - Connecting to the database retries 3 times by default
# 2019/03/06 (Simon) - Added InputValidator and ContentRenderer helper classes
#                    - Added error logging to separate file
# 2019/03/07 (Simon) - Added class ViewApplication for handling /applications
# 2019/03/13 (Simon) - Methods approve+reject+view implemented in ViewApplication
#                    - Split affiliation input validation in AddRecord.insert() to be used by other methods
#                    - Program reads db.conf for the SQL server settings by default


import os                               # for accessing the filesystem
from collections import defaultdict     # for handling inputs with a single dict object
import mysql.connector                  # for accessing the MySQL database
from datetime import date, datetime     # for getting the current date
from uuid import uuid4                  # for creating a unique ID for database insertion
import re                               # for input validation
import cherrypy                         # for exposing python as a webserver
import atexit                           # for handling server exit condition
from mako.template import Template      # for rendering dynamic content through templating
from mako.lookup import TemplateLookup


#
# HELPER METHODS
#

# returns a string-type unique id
def newID():
    return str(uuid4())

# returns an integer if the input string s
# is a valid integer, returns False otherwise;
# used for input validation of int-type inputs
# parameters:
#   (string type) s
def toInt(s):
    try:
        int(s)
    except:
        return False
    return int(s)
    
#
def today(hasTime=True):
    if hasTime:
        return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return (datetime.now().strftime("%Y-%m-%d"))


#
# HELPER CLASSES
#
    
# class handling a single persistent SQL database connection
# class parameters:
#   (dict type) config      - SQL database configuration
# methods:
#   connect(retries=0)     - connects to an SQL database using the config
#   disconnect()           - disconnects previous connection, if any
class DBConnection(object):
    def __init__(self, arg=None):
        self.connection = None
        # default configuration for connecting to a MySQL server
        if arg is None:
            self.config = {
              'user': 'cs192',
              'password': 'cs192',
              'host': '127.0.0.1',
              'database': 'mydb',
              'raise_on_warnings': True
            }
        # use the passed config if given
        else:
            self.config = arg
    
    # for checking if there is still a connection to the database
    # returns True if connected, False otherwise
    def is_connected(self):
        if self.connection is None:
            return False
        return self.connection.is_connected()
    
    # handles connecting to the database
    # returns the connection object, or None if it failed to connect
    def connect(self, retries=3):
        # try connecting to the SQL server if not yet connected, handling any exceptions
        ctr = 0
        # keep trying to connect
        while (self.connection is None) and (ctr <= retries):
            try:
                self.connection = mysql.connector.connect(option_files=self.config)
                if self.is_connected():
                    # return object for interacting with the SQL database
                    cherrypy.log.error("Connected to SQL database")
                    return self.connection
            except mysql.connector.Error as err:
                if ctr == retries:
                    # wrong database user+pdbassword
                    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                        cherrypy.log.error("Error: Something is wrong with your user name or password")
                    # non-existent database
                    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                        cherrypy.log.error("Error: Database does not exist")
                    # everything else
                    else:
                        cherrypy.log.error("Error: ", err)
                self.connection = None
                ctr += 1
        # check if previous SQL connection is still connected
        if self.connection is not None:
            if self.connection.is_connected():
                # return object for interacting with the SQL database
                return self.connection
        # only executes if not yet connected for the first time
        cherrypy.log.error("Error: Cannot connect to SQL database")
        return None
    
    # disconnects from the database
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
        cherrypy.log.error("Disconnected from SQL database")
        return
        
# class handling input validation
# class parameters:
#   None
# methods:
#   setLimits(fields): set limits for input validator
#   (dict/str/None) fields  - which input fields to validate
#                   * (if dict type)
#                       - key: (str type) input field name
#                       - value: (tuple type) limits
#                           - 0: field minimum (inclusive)
#                           - 1: field maximum (inclusive)
#                           - 2: is the field required?
#                   * (if str type) valid preset strings:
#                       - "record", "affiliation", "application", "application_renew"
#   validate(inputs,skip=[])    - validate inputs, while skipping any key in list
#                               - expects:
#                                   - (dict) inputs: key:<name>, value:<field value>
#                                   - (list) skip: <name>
class InputValidator(object):
    # preset input field limits
    record_dict = {
        'region':       (1,17,True),
        'level':        (1,4,True),
        'type':         (1,2,True),
        'school':       (2,100,True),
        'clubName':     (2,100,True),
        'address':      (2,200,True),
        'city':         (2,45,True),
        'province':     (2,45,True),
        'adviserName':  (1,100,True),
        'contact':      (4,45,True),
        'email':        (0,45,True)
    }
    affiliation_dict = {
        'affiliated':           (0,1,True),
        'status':               (0,45,False),
        'hasAffiliationForms':  (0,1,True),
        'benefits':             (0,200,False),
        'remarks':              (0,200,False),
        'schoolYear':           (2007,2050,True),
        'yearsAffiliated':      (1,50,True),
        'SCA':                  (1,32767,True),
        'SCM':                  (1,32767,True),
        'paymentMode':          (0,200,False),
        'paymentID':            (0,200,False),
        'paymentAmount':        (0,1000000000,False),
        'receiptNumber':        (0,200,False),
        'paymentSendMode':      (0,200,False)
    }
    application_dict = {
        'hasRecord':            (0,1,False)
    }
    
    def __init__(self):
        self.setLimits()
    
    def setLimits(self, arg=None):
        self.limits = defaultdict(lambda: None)
        # checking if using preset or custom limits
        if arg is None:
            self.limits.update({
                **self.record_dict, 
                **self.affiliation_dict,
                **self.application_dict
            })
        elif type(arg) is str:
            if arg is "record":
                self.limits.update({
                    **self.record_dict,
                    **self.affiliation_dict
                })
            elif arg is "affiliation":
                self.limits.update({
                    **self.affiliation_dict
                })
            elif arg is "application":
                self.limits.update({
                    **self.record_dict,
                    **self.affiliation_dict,
                    **self.application_dict
                })
            elif arg is "application_renew":
                self.limits.update({
                    **self.affiliation_dict,
                    **self.application_dict
                })
        else:
            self.limits.update(arg)
    
    # for validating dict-type object "inputs"
    # returns a list of errors (empty list if none)
    # each error is a tuple (error_message, field_name, field_value)
    def validate(self, inputs, skip=[]):
        errors = []
        if self.limits is None:
            return errors
        # iterate through the "inputs" dict
        for key, val in inputs.items():
            if key in skip:
                continue
            # skip item if it doesn't have defined limits
            if self.limits[key] is None:
                continue
            # get limits
            min,max,required = self.limits[key]
            # check if item is None or an empty string
            if required:
                if val is None:
                    errors.append(("Missing input", key, val))
                elif type(val) is str:
                    if len(val) == 0:
                        errors.append(("Missing input", key, val))
            # check if item is within limits
            if type(val) is int:
                if not(min <= val <= max):
                    errors.append(("Invalid length", key, val))
            elif type(val) is str:
                if not(min <= len(val) <= max):
                    errors.append(("Invalid length", key, val))
            # if current field item is "email", check if it has a valid format
            if key is "email":
                email_pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
                email_match = re.match(email_pattern, val, re.M) 
                if not email_match:
                    errors.append(("Invalid email address", key, val))
            # if current field item is "paymentDate", check if it has a valid format and is a valid past date
            elif key is "paymentDate":
                # date comparison assumes ISO format: yyyy-mm-dd
                date_pattern = r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
                date_match = re.match(date_pattern, val, re.M)
                if not date_match:
                    errors.append(("Invalid date (format is )", key, val))
                if (str(val) > str(today(hasTime=False))):
                    errors.append(("date_future", key, val))
        return errors

# persistent class handling Mako template rendering
# class parameters:
#   None
# methods:
#   render(templatefile, templatevars=None): return rendered HTML
#       (string type) templatefile (required) - name of template file
#       (dict type) templatevars - dict of variables ("name":"value") to pass to Mako
class ContentRenderer(object):
    def __init__(self):
        self.lookup = TemplateLookup(
            directories=["templates/"],
            collection_size=100,
            format_exceptions=True,
            module_directory="tmp/mako_modules"
        )
    def render(self, templatefile, templatevars=None):
        t = self.lookup.get_template(templatefile)
        if (templatevars is None):
            return t.render()
        return t.render(**templatevars)


#
# CHERRYPY-EXPOSED CLASSES
#

# class used by CherryPy to handle HTTP requests for /
class Root(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        self.renderer = Renderer
        # class handling /view
        self.view = ViewRecord(DBC=DBC, Renderer=Renderer)
        # class handling /add
        self.add = AddRecord(DBC=DBC, Renderer=Renderer, Validator=Validator)
        # class handling /apply
        self.apply = AddApplication(DBC=DBC, Renderer=Renderer, Validator=Validator)
        # class handling /applications
        self.applications = ViewApplication(DBC=DBC, Renderer=Renderer, Validator=Validator)
    
    @cherrypy.expose
    # CherryPy method handling /
    def index(self):
        # returns Mako-rendered homepage HTML
        return self.renderer.render("index.mako")

# class used by CherryPy for handling /view
@cherrypy.popargs('record_id', 'affiliation_id')
class ViewRecord(object):
    def __init__(self, DBC=None, Renderer=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()
        
    @cherrypy.expose
    # CherryPy method handling /view
    def index(self, q="", record_id=None, affiliation_id=None):
        if record_id is None:
            sqlcnx = self.DBC.connect()                     # connect to SQL server
            cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
            # fetch all columns from all rows in AffiliationRecordsTable
            if (len(q) == 0):
                cur.execute(
                    "SELECT clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                    "FROM AffiliationRecordsTable"
                )
            # fetch all columns from rows matching a query(filter) in AffiliationRecordsTable
            else:
                cur.execute(
                    "SELECT clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                    "FROM AffiliationRecordsTable "
                    "WHERE LOWER(school) LIKE %(query)s or "
                    "LOWER(clubName) LIKE %(query)s or "
                    "LOWER(address) LIKE %(query)s or "
                    "LOWER(city) LIKE %(query)s or "
                    "LOWER(province) LIKE %(query)s or "
                    "LOWER(adviserName) LIKE %(query)s", {"query":"%"+q+"%"}
                )
            res = cur.fetchall()
            # close database cursor
            cur.close()
            # create (list of dicts) data_list from (list of tuples) res
            data_list = []
            for record in res:
                record_dict = {
                    'clubID':       record[0],
                    'dateUpdated':  record[1],
                    'region':       record[2],
                    'level':        record[3],
                    'type':         record[4],
                    'school':       record[5],
                    'clubName':     record[6],
                    'address':      record[7],
                    'city':         record[8],
                    'province':     record[9],
                    'adviserName':  record[10],
                    'contact':      record[11],
                    'email':        record[12]
                }
                data_list.append(record_dict)
            # returns Mako-rendered view page HTML
            # (control ViewAffiliationRecordList)
            return self.renderer.render("view.mako", {"data":data_list, "q":q})
            
        else:
            # (control ViewAffiliationRecord)
            
            if affiliation_id is None:
                # Handles /view/<record_id>/
                # should return details about the affiliation record
                return "record id: %s" % record_id
            else:
                # Handles /view/<record_id>/<affiliation_id>
                # should return details about a specific affiliation within a club's record
                return "record id: %s<br>affiliation id: %s" % (record_id, affiliation_id)

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
    # CherryPy method handling /add/
    def index(self):
        # returns Mako-rendered add page HTML
        return self.renderer.render("add.mako")
    
    @cherrypy.expose
    # CherryPy method handling /add/insert with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    def insert(self, region, level, type, school, clubname, address, city, province, advisername, contact, email, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        # string format for inserting record_data into SQL database
        # table structure is defined in db.sql
        add_record = (
            "INSERT INTO AffiliationRecordsTable "
            "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
            "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)"
        )
        
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        id = newID()    # generate new unique ID for record_data
        record_data = {
            'clubID':       id,
            'dateUpdated':  today(),
            'region':       toInt(region),
            'level':        toInt(level),
            'type':         toInt(type),
            'school':       school,
            'clubName':     clubname,
            'address':      address,
            'city':         city,
            'province':     province,
            'adviserName':  advisername,
            'contact':      contact,
            'email':        email
        }
        
        # input validation
        self.validator.setLimits("record")
        errors = self.validator.validate(record_data)
        # display errors, if any
        if len(errors) > 0:
            cur.close() # close database cursor
            errortext = ""
            for e in errors:
                errortext += "["+str(e[0])+"] '"+str(e[1])+"': "+str(e[2])+"<br>"
            return self.renderer.render("dialog.mako", {
                'title': "Error!",
                'message': "Invalid affiliation record data:<br>"+errortext,
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back"
            })
        # checking for preexisting record
        collision_query = 'SELECT school, clubName FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s'
        cur.execute(collision_query, {'school': school, 'clubName': clubname})
        if cur.rowcount > 0:
            cur.close() # close database cursor
            return self.renderer.render("dialog.mako", {
                'title': "Error!",
                'message': "A matching record already exists in the database.",
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back"
            })
        res = self.validate_affiliation(id, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode)
        if len(res) > 0:
            cur.close() # close database cursor
            errortext = ""
            for e in res:
                errortext += "["+str(e[0])+"] '"+str(e[1])+"': "+str(e[2])+"<br>"
            return self.renderer.render("dialog.mako", {
                'title': "Error!",
                'message': "Invalid affiliation record data:<br>"+errortext,
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back"
            })
        cur.execute(add_record, record_data)            # insert record_data to database
        sqlcnx.commit()                                 # commit changes to database
        cur.close() # close database cursor
        self.insert_affiliation(id, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode)
        return self.renderer.render("dialog.mako", {           # return insertion success HTML
            'title': "Affiliation record added.",
            'linkaddr': "/add",
            'linktext': "Add another record"
        })
            
    def validate_affiliation(self, clubid, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        affiliation_data = {
            'affiliationID':                    newID(),    # generate new unique ID for affiliation_data
            'affiliated':                       toInt(affiliated),
            'status':                           status,
            'hasAffiliationForms':              toInt(hasaffiliationforms),
            'benefits':                         benefits,
            'remarks':                          remarks,
            'schoolYear':                       toInt(schoolyear),
            'yearsAffiliated':                  toInt(yearsaffiliated),
            'SCA':                              toInt(sca),
            'SCM':                              toInt(scm),
            'paymentMode':                      paymentmode,
            'paymentDate':                      paymentdate,
            'paymentID':                        paymentid,
            'paymentAmount':                    toInt(paymentamount),
            'receiptNumber':                    receiptnumber,
            'paymentSendMode':                  paymentsendmode,
            'AffiliationRecordsTable_clubID':   clubid
        }
        # input validation
        self.validator.setLimits("affiliation")
        errors = self.validator.validate(affiliation_data)
        return errors
        
    def insert_affiliation(self, clubid, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        # string format for inserting affiliation_data into SQL database
        # table structure is defined in db.sql
        add_affiliation = (
            "INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)"
        )
        affiliation_data = {
            'affiliationID':                    newID(),    # generate new unique ID for affiliation_data
            'affiliated':                       toInt(affiliated),
            'status':                           status,
            'hasAffiliationForms':              toInt(hasaffiliationforms),
            'benefits':                         benefits,
            'remarks':                          remarks,
            'schoolYear':                       toInt(schoolyear),
            'yearsAffiliated':                  toInt(yearsaffiliated),
            'SCA':                              toInt(sca),
            'SCM':                              toInt(scm),
            'paymentMode':                      paymentmode,
            'paymentDate':                      paymentdate,
            'paymentID':                        paymentid,
            'paymentAmount':                    toInt(paymentamount),
            'receiptNumber':                    receiptnumber,
            'paymentSendMode':                  paymentsendmode,
            'AffiliationRecordsTable_clubID':   clubid
        }
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        cur.execute(add_affiliation, affiliation_data)  # insert affiliation_data to database
        sqlcnx.commit()                                 # commit changes to database
        cur.close() # close database cursor

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
        check_error = None
        if toInt(hasrecord) is 1:
            collision_query = (
                "SELECT clubID, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                "FROM AffiliationRecordsTable WHERE clubID = %(clubID)s"
            )
            cur.execute(collision_query, {'clubID': clubid})
            if cur.rowcount == 1:
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
                check_error = ("Club with ID does not exist", "clubID", clubid)
            else:
                check_error = ("More than one club with same ID", "clubID", clubid)
                
        if skip_record_check:
            errors = self.validator.validate(application_data, [*self.validator.record_dict])
        else:
            errors = self.validator.validate(application_data)
        
        if check_error is not None:
            errors.append(check_error)    
        
        # display errors, if any
        if len(errors) > 0:
            errortext = ""
            for e in errors:
                errortext += "["+str(e[0])+"] '"+str(e[1])+"': "+str(e[2])+"<br>"
            return self.renderer.render("dialog.mako", {
                'title': "Error!",
                'message': "Invalid inputs:<br>"+errortext,
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back"
            })
        cur.execute(add_application, application_data)  # insert application_data to database
        sqlcnx.commit()                                 # commit changes to database
        return self.renderer.render("dialog.mako", {           # return insertion success HTML
            'title': "Sent an application.",
            'message': "",
        })
        cur.close() # close database cursor

# class used by CherryPy for handling /applications
class ViewApplication(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()
        if Validator is not None:
            self.validator = Validator
        else:
            self.validator = InputValidator()
        
    @cherrypy.expose
    # CherryPy method handling /applications
    def index(self, q=""):
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        # fetch all columns from all rows in AffiliationApplicationsTable
        if (len(q) == 0):
            cur.execute(
                "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
                "FROM AffiliationApplicationsTable"
            )
        # fetch all columns from rows matching a query(filter) in AffiliationApplicationsTable
        else:
            cur.execute(
                "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
                "FROM AffiliationApplicationsTable "
                "WHERE LOWER(school) LIKE %(query)s or "
                "LOWER(clubName) LIKE %(query)s or "
                "LOWER(address) LIKE %(query)s or "
                "LOWER(city) LIKE %(query)s or "
                "LOWER(province) LIKE %(query)s or "
                "LOWER(adviserName) LIKE %(query)s", {"query":"%"+q+"%"}
            )
        res = cur.fetchall()
        # close database cursor
        cur.close()
        # create (list of dicts) data_list from (list of tuples) res
        data_list = []
        for app in res:
            app_dict = {
                "appID"             :app[0], 
                "hasRecord"         :app[1], 
                "clubID"            :app[2], 
                "dateCreated"       :app[3], 
                "region"            :app[4], 
                "level"             :app[5], 
                "type"              :app[6], 
                "school"            :app[7], 
                "clubName"          :app[8], 
                "address"           :app[9], 
                "city"              :app[10], 
                "province"          :app[11], 
                "adviserName"       :app[12], 
                "contact"           :app[13], 
                "email"             :app[14], 
                "schoolYear"        :app[15], 
                "yearsAffiliated"   :app[16], 
                "SCA"               :app[17], 
                "SCM"               :app[18], 
                "paymentMode"       :app[19], 
                "paymentDate"       :app[20], 
                "paymentID"         :app[21], 
                "paymentAmount"     :app[22], 
                "receiptNumber"     :app[23], 
                "paymentSendMode"   :app[24]
            }
            data_list.append(app_dict)
        # returns Mako-rendered view page HTML
        # (control ViewAffiliationApplicationList)
        return self.renderer.render("approve.mako", {"data":data_list, "q":q})
        
    # Handles /applications/view/<application_id>/
    # should return details about the affiliation application
    @cherrypy.expose
    def view(self, application_id):
        return "app id: %s" % application_id
    
    # Handles /applications/approve/<application_id>/
    # creates a record from an affiliation application
    @cherrypy.expose
    def approve(self, application_id):
        a = AddRecord(DBC=self.DBC, Renderer=self.renderer, Validator=self.validator)
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        cur.execute(
            "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
            "FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":application_id}
        )
        app = cur.fetchone()
        cur.close()
        apd = {
            "appID"             :app[0], 
            "hasRecord"         :app[1], 
            "clubID"            :app[2],
            "dateCreated"       :app[3], 
            "region"            :app[4], 
            "level"             :app[5], 
            "type"              :app[6], 
            "school"            :app[7], 
            "clubName"          :app[8], 
            "address"           :app[9], 
            "city"              :app[10], 
            "province"          :app[11], 
            "adviserName"       :app[12], 
            "contact"           :app[13], 
            "email"             :app[14], 
            "schoolYear"        :app[15], 
            "yearsAffiliated"   :app[16], 
            "SCA"               :app[17], 
            "SCM"               :app[18], 
            "paymentMode"       :app[19], 
            "paymentDate"       :app[20], 
            "paymentID"         :app[21], 
            "paymentAmount"     :app[22], 
            "receiptNumber"     :app[23], 
            "paymentSendMode"   :app[24]
        }
        if toInt(apd["hasRecord"]) == 0:
            a.insert(apd["region"], apd["level"], apd["type"], apd["school"], apd["clubName"], apd["address"], apd["city"], apd["province"], apd["adviserName"], apd["contact"], apd["email"], "1", "", "1", "", "", apd["schoolYear"], apd["yearsAffiliated"], apd["SCA"], apd["SCM"], apd["paymentMode"], apd["paymentDate"], apd["paymentID"], apd["paymentAmount"], apd["receiptNumber"], apd["paymentSendMode"])
            cur = sqlcnx.cursor(buffered=True)
            cur.execute("SELECT clubID FROM AffiliationRecordsTable WHERE "
                "school = %(school)s AND clubName = %(clubName)s AND "
                "address = %(address)s AND region = %(region)s",
                {
                    "school":   apd["school"],
                    "clubName": apd["clubName"],
                    "address":  apd["address"],
                    "region":   apd["region"]
                }
            )
            apd["clubID"] = cur.fetchone()
            cur.close()
        else:
            a.insert_affiliation(apd["clubID"], "1", "", "1", "", "", apd["schoolYear"], apd["yearsAffiliated"], apd["SCA"], apd["SCM"], apd["paymentMode"], apd["paymentDate"], apd["paymentID"], apd["paymentAmount"], apd["receiptNumber"], apd["paymentSendMode"])
        cur = sqlcnx.cursor(buffered=True)
        cur.execute(
            "DELETE FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":apd["appID"]}
        )
        sqlcnx.commit()
        cur.close()
        return self.renderer.render("dialog.mako", {           # return deletion success HTML
            'title': "Approved application.",
            'message': "",
            'linkaddr': "/applications",
            'linktext': "&lt; Back to pending applications"
        })
    
    # Handles /applications/reject/<application_id>/
    # deletes an affiliation application
    @cherrypy.expose
    def reject(self, application_id=None):
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        cur.execute(
            "DELETE FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":application_id}
        )
        sqlcnx.commit()
        cur.close()
        return self.renderer.render("dialog.mako", {           # return deletion success HTML
            'title': "Rejected application.",
            'message': "",
        })




#
# MAIN METHOD
#

def main():
    # configuration of CherryPy webserver
    if __name__ == '__main__':
        print("Running server")
        cherrypy.config.update({
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'log.screen': False,
            'log.error_file': 'error.log',
            'log.access_file': 'access.log',
            'tools.gzip.on': True
        })
        
        # initialize persistent renderer & validator classes
        renderer = ContentRenderer()
        validator = InputValidator()
        
        # start a persistent connection to the SQL database
        dbc = DBConnection("db.conf")
        dbc.connect()
        
        # disconnect from SQL database on exit
        atexit.register(lambda d: d.disconnect(), dbc)
        
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './static'
            },
            '/styles': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './styles'
            },
            '/scripts': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './scripts'
            },
            '/favicon.ico':{
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.abspath("static/favicon.ico")
            }
        }
        # start the webserver
        cherrypy.quickstart(Root(dbc, renderer, validator), '/', conf)
        print("\nServer exited")

# start the program
main()
