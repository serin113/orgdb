# Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/02/06 - Initial working code and documentation
# 2019/02/08 - Updated CherryPy config, added getContent()


import os                               # for accessing the filesystem
import mysql.connector                  # for accessing the MySQL database
from datetime import date, datetime     # for getting the current date
from uuid import uuid4                  # for creating a unique ID for database insertion
import cherrypy                         # library responsible for exposing python as a webserver
import re                               # for input validation

# returns a string-type
def newID():
    return str(uuid4())

# returns an integer if the input string s
# is a valid integer, returns False otherwise;
# used for input validation of int-type inputs
def toInt(s):
    try:
        int(s)
    except:
        return False
    return int(s)

# return the contents of file s if it exists,
# return an error message otherwise
def getContent(s):
    if (os.path.isfile(s)):
        return open(s,"r").read()
    return "File \""+s+"\" does not exist"

# class used by CherryPy to handle HTTP requests for / or /index.html
class AffiliationDB(object):
    def __init__(self):
        self.view = ViewRecord()        # class handling /view
        self.addrecord = AddRecord()    # class handling /addrecord
        
    @cherrypy.expose
    def index(self):                    # CherryPy method handling /
        return getContent("index.html") # should return the homepage HTML

# class used by CherryPy for handling /view
class ViewRecord(object):
    def __init__(self):
        self.r = AffiliationRecord()    # class handling /view/r/
    
    @cherrypy.expose
    def index(self):                    # CherryPy method handling /view/r/
        # INSERT HERE
        return "<html><table>"                   # should return a list of viewable records
                                        # (control ViewAffiliationRecordList)

# class used by CherryPy for handling /view/r/<record_id>
@cherrypy.popargs('record_id')
class AffiliationRecord(object):
    def __init__(self):
        self.a = Affiliation()          # class handling /view/r/<record_id>/a
        
    @cherrypy.expose
    def index(self, record_id):             # CherryPy method handling /view/r/<record_id>/
        return "record id: %s" % record_id  # should return details about the affiliation record
                                            # (control ViewAffiliationRecord)

# class used by CherryPy for handling /r/<record_id>/a/<affiliation_id>
@cherrypy.popargs('affiliation_id')
class Affiliation(object):
    # CherryPy method handling /r/<record_id>/a/<affiliation_id>/
    @cherrypy.expose
    def index(self, record_id, affiliation_id):
        # should return details about a specific affiliation within a club's record
        # (control ViewAffiliationRecord)
        return "record id: %s<br>affiliation id: %s" % (record_id, affiliation_id)

# class used by CherryPy for handling /addrecord
class AddRecord(object):
    @cherrypy.expose
    def index(self):                        # CherryPy method handling /add/
        return getContent("addrecord.html") # returns entirety of addrecord.html
    
    # CherryPy method handling /add/insert with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    @cherrypy.expose
    def insert(self, region, level, type, school, clubname, address, city, province, advisername, contact, email, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        
        # string format for inserting record_data into SQL database
        # table structure is defined in db.sql
        add_record = ("INSERT INTO AffiliationRecordsTable "
            "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
            "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)")
        
        # string format for inserting affiliation_data into SQL database
        # table structure is defined in db.sql
        add_affiliation = ("INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)")
        
        # input validation
        
        # validates data for record_data
        if not(1 <= toInt(region) <= 17) or not(1 <= toInt(level) <= 4) or not(1 <= toInt(type) <= 2) or (len(school) > 100) or (len(clubname) > 100) or (len(address) > 200) or (len(city) > 45) or (len(province) > 45) or (len(advisername) > 100) or (len(contact) > 45) or (len(email) > 45):
            return "<h1>Invalid affiliation record data</h1>"
        today = date.today()
        # validates data for affiliation_data
        if not(2007 <= toInt(schoolyear) <= 2050) or not(0 <= toInt(affiliated) <= 1) or (len(status) > 45) or not(0 <= toInt(hasaffiliationforms) <= 1) or (len(benefits) > 100) or (len(remarks) > 200) or not(1 <= toInt(yearsaffiliated) <= 50) or not(1 <= toInt(sca) <= 100) or not(1 <= toInt(scm) <= 2000) or (len(paymentmode) > 200) or (str(paymentdate) > str(today)) or (len(paymentid) > 200) or (toInt(paymentamount) < 0) or (len(receiptnumber) > 200) or (len(paymentsendmode) > 200):
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

        sqlcnx = connectDB()                            # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database

        collision_query = 'SELECT school, clubName FROM AffiliationRecordsTable WHERE school = %(school)s AND clubName = %(clubName)s'
        cur.execute(collision_query, {'school': school, 'clubName': clubname})

        if cur.rowcount > 0:
            return "<h1>Invalid affiliation data: Record already exists</h1>"

        
        
        id = newID()    # generate new unique ID for record_data
        record_data = {
            'clubID':       id,
            'dateUpdated':  today,
            'region':       region,
            'level':        level,
            'type':         type,
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
            'affiliated':                       affiliated,
            'status':                           status,
            'hasAffiliationForms':              hasaffiliationforms,
            'benefits':                         benefits,
            'remarks':                          remarks,
            'schoolYear':                       schoolyear,
            'yearsAffiliated':                  yearsaffiliated,
            'SCA':                              sca,
            'SCM':                              scm,
            'paymentMode':                      paymentmode,
            'paymentDate':                      paymentdate,
            'paymentID':                        paymentid,
            'paymentAmount':                    paymentamount,
            'receiptNumber':                    receiptnumber,
            'paymentSendMode':                  paymentsendmode,
            'AffiliationRecordsTable_clubID':   id
        }
        
        
        cur.execute(add_record, record_data)            # insert record_data to database
        cur.execute(add_affiliation, affiliation_data)  # insert affiliation_data to database
        sqlcnx.commit()                                 # commit changes to database
        cur.close()                                     # close cursor to the database
        sqlcnx.close()                                  # close connection to SQL server
        
        return "<h1>Affiliation record added</h1>"      # should return insertion success HTML

# method that handles the connection to the database
def connectDB():
    # default configuration for connecting to a MySQL server
    DBConfig = {
      'user': 'orgdb',
      'password': 'orgdb',
      'host': '127.0.0.1',
      'database': 'mydb',
      'raise_on_warnings': True
    }
    
    # try connecting to the SQL server, handling any exceptions
    try:
        cnx = mysql.connector.connect(**DBConfig)
    except mysql.connector.Error as err:
        # wrong database user+pdbassword
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        # non-existent database
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        # everything else
        else:
            print(err)
    else:
        # return object for interacting with the SQL database
        return cnx


# main method handling program execution
def main():
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
            '/favicon.ico':{
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.abspath("favicon.ico")
            }
        }
        cherrypy.quickstart(AffiliationDB(), '/', conf)

main()
    
