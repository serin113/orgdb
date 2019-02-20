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


import os                               # for accessing the filesystem
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

# return the contents of file s if it exists,
# return an error message otherwise 
# parameters:
#   (string type) templateFile (required) - name of template file
#   (dict type) templatevars - dict of variables ("name":"value") to pass to Mako
templatelookup = TemplateLookup(
    directories=["templates/"],
    collection_size=100,
    format_exceptions=True,
    module_directory="tmp/mako_modules"
)
def renderContent(templatefile, templatevars=None):
    global templatelookup
    t = templatelookup.get_template(templatefile)
    if (templatevars is None):
        return t.render()
    return t.render(**templatevars)


#
# HELPER CLASSES
#
    
# class handling a single SQL database connection
# class parameters:
#   (dict type) config      - SQL database configuration
# methods:
#    connect(retries=0)     - connects to an SQL database using the config
#    disconnect()           - disconnects previous connection, if any
class DBConnection(object):
    def __init__(self, arg=None):
        self.connection = None
        # default configuration for connecting to a MySQL server
        if arg is None:
            self.config = {
              'user': 'orgdb',
              'password': 'orgdb',
              'host': '127.0.0.1',
              'database': 'mydb',
              'raise_on_warnings': True
            }
        else:
            self.config = arg
    # method that handles the connection to the database
    def is_connected(self):
        return self.connection.is_connected()
    def connect(self, retries=3):
        # try connecting to the SQL server if not yet connected, handling any exceptions
        ctr = 0
        # keep trying to connect
        while (self.connection is None) and (ctr <= retries):
            try:
                self.connection = mysql.connector.connect(**self.config)
                if self.is_connected():
                    # return object for interacting with the SQL database
                    print("Connected to SQL database")
                    return self.connection
            except mysql.connector.Error as err:
                if ctr == retries:
                    # wrong database user+pdbassword
                    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Error: Something is wrong with your user name or password")
                    # non-existent database
                    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                        print("Error: Database does not exist")
                    # everything else
                    else:
                        print("Error: ", err)
                self.connection = None
                ctr += 1
        # check if previous SQL connection is still connected
        if self.connection is not None:
            if self.connection.is_connected():
                return self.connection
        print("Error: Cannot connect to SQL database")
        return None
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
        print("Disconnected from SQL database")
        return


#
# CHERRYPY-EXPOSED CLASSES
#

# class used by CherryPy to handle HTTP requests for /
class Root(object):
    def __init__(self, DBC):
        self.view = ViewRecord(DBC)        # class handling /view
        self.add = AddRecord(DBC)          # class handling /add
    
    @cherrypy.expose
    def index(self):                    # CherryPy method handling /
        # returns Mako-rendered homepage HTML
        return renderContent("index.mako")

# class used by CherryPy for handling /view
@cherrypy.popargs('record_id', 'affiliation_id')
class ViewRecord(object):
    def __init__(self, DBC=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        
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
            return renderContent("view.mako", {"data":data_list, "q":q})
            
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
    def __init__(self, DBC=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
    
    @cherrypy.expose
    # CherryPy method handling /add/
    def index(self):
        # returns Mako-rendered add page HTML
        return renderContent("add.mako")
    
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
        
        # string format for inserting affiliation_data into SQL database
        # table structure is defined in db.sql
        add_affiliation = (
            "INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)"
        )
        
        # input validation
        
        # validates data for record_data
        if not(1 <= toInt(region) <= 17) or \
            not(1 <= toInt(level) <= 4) or \
            not(1 <= toInt(type) <= 2) or \
            (len(school) > 100) or \
            (len(clubname) > 100) or \
            (len(address) > 200) or \
            (len(city) > 45) or \
            (len(province) > 45) or \
            (len(advisername) > 100) or \
            (len(contact) > 45) or \
            (len(email) > 45):
            return "<h1>Invalid affiliation record data</h1>"
            
        today = date.today()
        # validates data for affiliation_data
        if not(2007 <= toInt(schoolyear) <= 2050) or \
            not(0 <= toInt(affiliated) <= 1) or \
            (len(status) > 45) or \
            not(0 <= toInt(hasaffiliationforms) <= 1) or \
            (len(benefits) > 100) or \
            (len(remarks) > 200) or \
            not(1 <= toInt(yearsaffiliated) <= 50) or \
            not(1 <= toInt(sca) <= 100) or \
            not(1 <= toInt(scm) <= 2000) or \
            (len(paymentmode) > 200) or\
            (str(paymentdate) > str(today)) or \
            (len(paymentid) > 200) or\
            not(toInt(paymentamount) >= 0) or\
            (len(receiptnumber) > 200) or\
            (len(paymentsendmode) > 200):
            return "<h1>Invalid affiliation data</h1>"
        
        # date comparison assumes ISO format: yyyy-mm-dd
        # date validation
        date_pattern = r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
        date_match = re.match(date_pattern, paymentdate, re.M)
        if not date_match:
            return "<h1>Invalid affiliation data</h1>"
        
        # email validation
        email_pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
        email_match = re.match(email_pattern, email, re.M) 
        if not email_match:
            return "<h1>Invalid affiliation data</h1>"
        
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database

        # checking for preexisting record
        collision_query = 'SELECT school, clubName FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s'
        cur.execute(collision_query, {'school': school, 'clubName': clubname})
        if cur.rowcount > 0:
            return "<h1>Invalid affiliation data: Record already exists</h1>"
        
        id = newID()    # generate new unique ID for record_data
        record_data = {
            'clubID':       id,
            'dateUpdated':  today,
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
            'AffiliationRecordsTable_clubID':   id
        }
        cur.execute(add_record, record_data)            # insert record_data to database
        cur.execute(add_affiliation, affiliation_data)  # insert affiliation_data to database
        sqlcnx.commit()                                 # commit changes to database
        cur.close()                                     # close cursor to the database
        return "<h1>Affiliation record added</h1>"      # should return insertion success HTML


#
# MAIN METHOD
#

def main():
    # start a persistent connection to the SQL database
    DBC = DBConnection()
    DBC.connect()
    
    # disconnect from SQL database on exit
    atexit.register(lambda dbc: dbc.disconnect(), DBC)
    
    # configuration of CherryPy webserver
    if __name__ == '__main__':
        cherrypy.config.update({
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
        })
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
        cherrypy.quickstart(Root(DBC), '/', conf)

# start the program
main()
