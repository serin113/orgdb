import random
import string
import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime

import cherrypy

#AffiliationRecord.type -> AffiliationRecord.isPublic

#python-cherrypy
#python-mysql-connector

#https://docs.cherrypy.org/en/latest/tutorials.html

#sudo systemctl start mariadb.service
#mysql -u root -p

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
    def insert(self, clubid, region, level, type, school, clubname, address, city, province, advisername, contact, email, affiliated, status, hasaffiliationforms, benefits, remarks, schoolyear, yearsaffiliated, sca, scm, paymentmode, paymentdate, paymentid, paymentamount, receiptnumber, paymentsendmode):
        
        add_record = ("INSERT INTO AffiliationRecordsTable "
            "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
            "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)")
        add_affiliation = ("INSERT INTO AffiliationTable "
            "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
            "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)")
        
        id = ''.join(random.sample(string.hexdigits, 8))
        record_data = {
            'clubID':       id,
            'dateUpdated':  date.today(),
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
            'affiliationID':                    random.randint(1,255),
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
        
    
    # @cherrypy.expose
    # def insertTest(self):
    #     add_record = ("INSERT INTO AffiliationRecordsTable "
    #         "(clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email) "
    #         "VALUES (%(clubID)s, %(dateUpdated)s, %(region)s, %(level)s, %(type)s, %(school)s, %(clubName)s, %(address)s, %(city)s, %(province)s, %(adviserName)s, %(contact)s, %(email)s)")
    #     add_affiliation = ("INSERT INTO AffiliationTable "
    #         "(affiliationID, affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode, AffiliationRecordsTable_clubID) "
    #         "VALUES (%(affiliationID)s, %(affiliated)s, %(status)s, %(hasAffiliationForms)s, %(benefits)s, %(remarks)s, %(schoolYear)s, %(yearsAffiliated)s, %(SCA)s, %(SCM)s, %(paymentMode)s, %(paymentDate)s, %(paymentID)s, %(paymentAmount)s, %(receiptNumber)s, %(paymentSendMode)s, %(AffiliationRecordsTable_clubID)s)")
    # 
    #     id = ''.join(random.sample(string.hexdigits, 8))
    # 
    #     record_data = {
    #         'clubID':       id,
    #         'dateUpdated':  date.today(),
    #         'region':       3,
    #         'level':        2,
    #         'type':         1,
    #         'school':       "JLD High School",
    #         'clubName':     "Club-Cluban",
    #         'address':      "Maginhawa",
    #         'city':         "Diliman",
    #         'province':     "Quezon City",
    #         'adviserName':  "Mahinhinan",
    #         'contact':      "0922228581",
    #         'email':        "jld@mani.la"
    #     }
    # 
    #     affiliation_data = {
    #         'affiliationID':                    234,
    #         'affiliated':                       True,
    #         'status':                           "newly affiliated",
    #         'hasAffiliationForms':              True,
    #         'benefits':                         "N/A",
    #         'remarks':                          "none",
    #         'schoolYear':                       2020,
    #         'yearsAffiliated':                  2,
    #         'SCA':                              1,
    #         'SCM':                              25,
    #         'paymentMode':                      "Delivery",
    #         'paymentDate':                      date(2019, 1, 15),
    #         'paymentID':                        "LBC-563R",
    #         'paymentAmount':                    20000,
    #         'receiptNumber':                    "BR-561",
    #         'paymentSendMode':                  "LBC",
    #         'AffiliationRecordsTable_clubID':   id
    #     }
    # 
    #     sqlcnx = connectDB()
    #     cur = sqlcnx.cursor()
    #     cur.execute(add_record, record_data)
    #     cur.execute(add_affiliation, affiliation_data)
    #     sqlcnx.commit()
    #     cur.close()
    #     sqlcnx.close()
        


def connectDB():
    config = {
      'user': 'orgdb',
      'password': 'orgdb',
      'host': '127.0.0.1',
      'database': 'mydb',
      'raise_on_warnings': True
    }
    try:
      cnx = mysql.connector.connect(**config)
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
    