# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
#                    - Fixed misplaced cur.close() statement


from ._helpers import *
from .AddRecord import *


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
        # create instance of AddRecord for insertion
        addrecord = AddRecord(DBC=self.DBC, Renderer=self.renderer, Validator=self.validator)
        sqlcnx = self.DBC.connect()                     # connect to SQL server
        cur = sqlcnx.cursor(buffered=True)              # create an SQL cursor to the database
        cur.execute(
            "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
            "FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":application_id}
        )
        app = cur.fetchone()    # fetch data
        cur.close()             # close database cursor
        # create dict for validation
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
        # if application indicates no existing record
        if toInt(apd["hasRecord"]) == 0:
            # insert data into AffiliationRecordsTable & AffiliationTable
            addrecord.insert(apd["region"], apd["level"], apd["type"], apd["school"], apd["clubName"], apd["address"], apd["city"], apd["province"], apd["adviserName"], apd["contact"], apd["email"], "1", "", "1", "", "", apd["schoolYear"], apd["yearsAffiliated"], apd["SCA"], apd["SCM"], apd["paymentMode"], apd["paymentDate"], apd["paymentID"], apd["paymentAmount"], apd["receiptNumber"], apd["paymentSendMode"])
            cur = sqlcnx.cursor(buffered=True)  # create SQL database cursor
            # get clubID of new record
            cur.execute(
                "SELECT clubID FROM AffiliationRecordsTable WHERE "
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
            cur.close()     # close database cursor
        # if application indicates an existing record with clubID
        else:
            # insert data into AffiliationTable
            addrecord.insert_affiliation(apd["clubID"], "1", "", "1", "", "", apd["schoolYear"], apd["yearsAffiliated"], apd["SCA"], apd["SCM"], apd["paymentMode"], apd["paymentDate"], apd["paymentID"], apd["paymentAmount"], apd["receiptNumber"], apd["paymentSendMode"])
        cur = sqlcnx.cursor(buffered=True)  # create SQL database cursor
        # delete application from AffiliationApplicationsTable (it's already approved)
        cur.execute(
            "DELETE FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":apd["appID"]}
        )
        sqlcnx.commit() # commit changes to database
        cur.close() # close database cursor
        return self.renderer.render("dialog.mako", {    # return approval success HTML
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
        # delete application from AffiliationApplicationsTable (no further action required)
        cur.execute(
            "DELETE FROM AffiliationApplicationsTable "
            "WHERE appID = %(appID)s", {"appID":application_id}
        )
        sqlcnx.commit() # commit changes to database
        cur.close() # close database cursor
        return self.renderer.render("dialog.mako", {    # return deletion success HTML
            'title': "Rejected application.",
            'message': "",
        })
