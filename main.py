import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from uuid import uuid4
import cherrypy
import re

#python-cherrypy
#python-mysql-connector
#https://docs.cherrypy.org/en/latest/tutorials.html

DBConfig = {
  'user': 'orgdb',
  'password': 'orgdb',
  'host': '127.0.0.1',
  'database': 'mydb',
  'raise_on_warnings': True
}

def newID():
    return str(uuid4())
    
def toInt(i):
    try:
        int(i)
    except:
        return False
    return int(i)

class AffiliationDB(object):
    def __init__(self):
        self.view = ViewRecord() #/view
        self.addrecord = AddRecord() #/addrecord
        
    @cherrypy.expose
    def index(self):
        return "Hello world"
        
class ViewRecord(object):
    def __init__(self):
        self.r = AffiliationRecord() #/view/r/
    
    @cherrypy.expose
    def index(self):
        return "um"
    
@cherrypy.popargs('record_id')    
class AffiliationRecord(object):
    def __init__(self):
        self.a = Affiliation()
        
    @cherrypy.expose
    # /r/<record_id>
    def index(self, record_id):
        return "record id: %s" % record_id

@cherrypy.popargs('affiliation_id')    
class Affiliation(object):
    @cherrypy.expose
    # /r/<record_id>/a/<affiliation_id>
    def index(self, record_id, affiliation_id):
        return "record id: %s<br>affiliation id: %s" % (record_id, affiliation_id)
        
class AddRecord(object):
    @cherrypy.expose
    def index(self):
        return open("addrecord.html","r").read()
    
    @cherrypy.expose
    def insert(self, region, level, type, school, clubname, address, city, province, advisername, contact, email, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        
        add_record = ("INSERT INTO AffiliationRecordsTable "
            "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
            "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)")
        add_affiliation = ("INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)")
        
        if not(1 <= toInt(region) <= 17) or not(1 <= toInt(level) <= 4) or not(1 <= toInt(type) <= 2) or (len(school) > 100) or (len(clubname) > 100) or (len(address) > 200) or (len(city) > 45) or (len(province) > 45) or (len(advisername) > 100) or (len(contact) > 45) or (len(email) > 45):
            return "<h1>Invalid affiliation record data</h1>"
        
        today = date.today()
       
        if not(2007 <= toInt(schoolyear) <= 2050) or not(0 <= toInt(affiliated) <= 1) or (len(status) > 45) or not(0 <= toInt(hasaffiliationforms) <= 1) or (len(benefits) > 100) or (len(remarks) > 200) or not(1 <= toInt(yearsaffiliated) <= 50) or not(1 <= toInt(sca) <= 100) or not(1 <= toInt(scm) <= 2000) or (len(paymentmode) > 200) or (str(paymentdate) > str(today)) or (len(paymentid) > 200) or (toInt(paymentamount) < 0) or (len(receiptnumber) > 200) or (len(paymentsendmode) > 200):
            return "<h1>Invalid affiliation data</h1>"

        # date comparison assumes ISO format: yyyy-mm-dd
        pattern = r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
        match = re.match(pattern, paymentdate, re.M)
        if not match:
            return "<h1>Invalid affiliation data</h1>"


        
        id = newID()
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
            'affiliationID':                    newID(),
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
        
        sqlcnx = connectDB()
        cur = sqlcnx.cursor()
        cur.execute(add_record, record_data)
        cur.execute(add_affiliation, affiliation_data)
        sqlcnx.commit()
        cur.close()
        sqlcnx.close()
        
        return "<h1>Affiliation record added</h1>"

def connectDB():
    global DBConfig
    try:
        cnx = mysql.connector.connect(**DBConfig)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("MySQL Connection: ", cnx.is_connected())
        return cnx


def main():
    if __name__ == '__main__':
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
        }
        cherrypy.quickstart(AffiliationDB(), '/', conf)

main()
    
