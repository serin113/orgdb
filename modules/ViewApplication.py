# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
#                    - Fixed misplaced cur.close() statement
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users
# 2019/03/29 (Simon) - "DBC" argument now indicates the database configuration settings
#                           instead of a DBConnection class
#                    - Database connection now handled using a with statement
# 2019/04/02 (Simon) - Fixed saved club if application indicates no existing record
#                    - Changed "back" URL
# 2019/04/05 (Simon) - Handle case of paymentDate being an empty string ""
#                    - clubID checking in approve() is handled with a separate DBConnection
# 2019/04/24 (Simon) - Convert dates to strings before displaying
#                    - Remove /view page handler
#                    - Change backlink in success/error dialog
#                    - Log more errors
# 2019/05/15 (Simon) - Added **kwargs to CherryPy-exposed methods to catch unexpected parameters w/o an error
# 2019/05/17 (Simon) - Added handling for missing affiliation_id case in approve() and reject()
#                    - Added benefits & remarks parameters in approve()
#                    - cursor.fetchall() returns dictionary list instead of tuple list when needed

from ._helpers import *
from .AddRecord import *
from .Login import *


# class used by CherryPy for handling /applications
class ViewApplication(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC_conf = DBC
            self.DBC = DBConnection(DBC)
        else:
            self.DBC_conf = "db.conf"
            self.DBC = DBConnection("db.conf")

        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()
        if Validator is not None:
            self.validator = Validator
        else:
            self.validator = InputValidator()

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @accessible_by("admin")
    # CherryPy method handling /applications
    def index(self, q="", **kwargs):
        with self.DBC as sqlcnx:
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database
            # fetch all columns from all rows in AffiliationApplicationsTable
            if (len(q) == 0):
                cur.execute(
                    "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
                    "FROM AffiliationApplicationsTable")
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
                    "LOWER(adviserName) LIKE %(query)s",
                    {"query": "%" + q + "%"})
            res = cur.fetchall()
            # close database cursor
            cur.close()
            # create (list of dicts) data_list from (list of tuples) res
            data_list = []
            for app in res:
                app_dict = {
                    "appID": app[0],
                    "hasRecord": app[1],
                    "clubID": app[2],
                    "dateCreated": app[3],
                    "region": app[4],
                    "level": app[5],
                    "type": app[6],
                    "school": app[7],
                    "clubName": app[8],
                    "address": app[9],
                    "city": app[10],
                    "province": app[11],
                    "adviserName": app[12],
                    "contact": app[13],
                    "email": app[14],
                    "schoolYear": app[15],
                    "yearsAffiliated": app[16],
                    "SCA": app[17],
                    "SCM": app[18],
                    "paymentMode": app[19],
                    "paymentID": app[21],
                    "paymentAmount": app[22],
                    "receiptNumber": app[23],
                    "paymentSendMode": app[24]
                }
                if app[20] is not None:
                    if len(str(app[20])) > 0:
                        app_dict["paymentDate"] = str(app[20])
                    else:
                        app_dict["paymentDate"] = None
                else:
                    app_dict["paymentDate"] = None
                data_list.append(app_dict)
            # returns Mako-rendered view page HTML
            # (control ViewAffiliationApplicationList)
            return self.renderer.render("applications.mako", {
                "data": data_list,
                "q": q,
                'user': getUserType(self.DBC)
            })
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })

    # Handles /applications/approve/<application_id>/
    # creates a record from an affiliation application
    @cherrypy.expose
    @accessible_by("admin")
    def approve(self, application_id=None, benefits=None, remarks=None, **kwargs):
        if application_id is None:
            cherrypy.log.error(
                "Warning (ViewApplication.approve): tried approving without application ID"
            )
            return self.renderer.render(
                "dialog.mako",
                {
                    'title': "Error!",
                    'message': "Invalid operation.",
                    'linkaddr': "#back",
                    'linktext': "< Back",
                    'user': getUserType(self.DBC)
                })
        with self.DBC as sqlcnx:
            # create instance of AddRecord for insertion
            addrecord = AddRecord(DBC=self.DBC.config,
                                  Renderer=self.renderer,
                                  Validator=self.validator)
            cur = sqlcnx.cursor(
                buffered=True, dictionary=True)  # create an SQL cursor to the database
            cur.execute(
                "SELECT appID, hasRecord, clubID, dateCreated, region, level, type, school, clubName, address, city, province, adviserName, contact, email, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
                "FROM AffiliationApplicationsTable "
                "WHERE appID = %(appID)s", {"appID": application_id})
            apd = cur.fetchone()  # fetch data
            cur.close()  # close database cursor
            if apd["paymentDate"] is not None:
                if len(str(apd["paymentDate"])) > 0:
                    apd["paymentDate"] = str(apd["paymentDate"])
                else:
                    apd["paymentDate"] = None
            else:
                apd["paymentDate"] = None
            hasRecord = toInt(apd["hasRecord"]) == 1
            # if application indicates no existing record
            if not hasRecord:
                # insert data into AffiliationRecordsTable & AffiliationTable
                addrecord._insert(apd["region"], apd["level"], apd["type"],
                                  apd["school"], apd["clubName"],
                                  apd["address"], apd["city"], apd["province"],
                                  apd["adviserName"], apd["contact"],
                                  apd["email"], "1", "new", "1", benefits, remarks,
                                  apd["schoolYear"], apd["yearsAffiliated"],
                                  apd["SCA"], apd["SCM"], apd["paymentMode"],
                                  apd["paymentDate"], apd["paymentID"],
                                  apd["paymentAmount"], apd["receiptNumber"],
                                  apd["paymentSendMode"])
                # fetch the clubID with a different (updated) database connection
                with DBConnection(self.DBC_conf) as sqlcnx2:
                    cur = sqlcnx2.cursor(
                        buffered=True)  # create SQL database cursor
                    # get clubID of new record
                    cur.execute(
                        "SELECT clubID FROM AffiliationRecordsTable WHERE "
                        "school = %(school)s AND clubName = %(clubName)s AND "
                        "address = %(address)s AND region = %(region)s AND "
                        "level = %(level)s AND type = %(type)s", {
                            "school": apd["school"],
                            "clubName": apd["clubName"],
                            "address": apd["address"],
                            "region": apd["region"],
                            "level": apd["level"],
                            "type": apd["type"]
                        })
                    res = cur.fetchone()
                    if res is not None:
                        apd["clubID"] = res[0]
                    cur.close()  # close database cursor
                    if res is None:
                        cherrypy.log.error(
                            "Error (ViewApplication.approve): failed to find recently inserted record"
                        )
                        return self.renderer.render(
                            "dialog.mako", {
                                'title': "Error!",
                                'message': "A database error occured.",
                                'linkaddr': "#back",
                                'linktext': "< Back",
                                'user': getUserType(self.DBC)
                            })
            # if application indicates an existing record with clubID
            else:
                # insert data into AffiliationTable
                addrecord.insert_affiliation(
                    apd["clubID"], "1", "renewing", "1", benefits, remarks, apd["schoolYear"],
                    apd["yearsAffiliated"], apd["SCA"], apd["SCM"],
                    apd["paymentMode"], apd["paymentDate"], apd["paymentID"],
                    apd["paymentAmount"], apd["receiptNumber"],
                    apd["paymentSendMode"])

            cur = sqlcnx.cursor(buffered=True)  # create SQL database cursor
            # delete application from AffiliationApplicationsTable (it's already approved)
            cur.execute(
                "DELETE FROM AffiliationApplicationsTable "
                "WHERE appID = %(appID)s", {"appID": apd["appID"]})
            sqlcnx.commit()  # commit changes to database
            cur.close()  # close database cursor
            return self.renderer.render(
                "dialog.mako",
                {  # return approval success HTML
                    'title': "Approved application.",
                    'message': "",
                    'linkaddr': "/view/" + str(apd["clubID"]),
                    'linktext': "< Go to record",
                    'linkaddr2': "/applications",
                    'linktext2': "< Back to pending applications",
                    'user': getUserType(self.DBC)
                })
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })

    # Handles /applications/reject/<application_id>/
    # deletes an affiliation application
    @cherrypy.expose
    @accessible_by("admin")
    def reject(self, application_id=None, **kwargs):
        if application_id is None:
            cherrypy.log.error(
                "Warning (ViewApplication.reject): tried rejecting without application ID"
            )
            return self.renderer.render(
                "dialog.mako",
                {
                    'title': "Error!",
                    'message': "Invalid operation.",
                    'linkaddr': "#back",
                    'linktext': "< Back",
                    'user': getUserType(self.DBC)
                })
        with self.DBC as sqlcnx:
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database
            # delete application from AffiliationApplicationsTable (no further action required)
            cur.execute(
                "DELETE FROM AffiliationApplicationsTable "
                "WHERE appID = %(appID)s", {"appID": application_id})
            sqlcnx.commit()  # commit changes to database
            cur.close()  # close database cursor
            return self.renderer.render(
                "dialog.mako",
                {  # return deletion success HTML
                    'title': "Rejected application.",
                    'message': "",
                    'user': getUserType(self.DBC)
                })
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })
