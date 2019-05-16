# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon)- Moved class to this file
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users
# 2019/03/29 (Simon) - "DBC" argument now indicates the database configuration settings
#                           instead of a DBConnection class
#                    - Database connection now handled using a with statement
# 2019/04/02 (Simon) - Changed "back" URL
# 2019/04/05 (Simon) - Removed redundant disconnect() calls
#                    - Added viewing individual record for logged-in club account
#                    - usertype in index() is checked before connecting to database for querying record info
# 2019/05/15 (Simon) - Added **kwargs to CherryPy-exposed methods to catch unexpected parameters w/o an error
#                    - Simplified usertype conditions in index()
#                    - Fetch affiliations from AffiliationTable for viewing individual record
# 2019/05/17 (Simon) - Fixed SQL query typo in index()

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /view/<record_id>
@cherrypy.popargs('record_id')
class ViewRecord(object):
    def __init__(self, DBC=None, Renderer=None):
        if DBC is not None:
            self.DBC = DBConnection(DBC)
        else:
            self.DBC = DBConnection("db.conf")
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @accessible_by(["club", "admin"])
    # CherryPy method handling /view/<record_id>
    def index(self, q="", record_id=None, **kwargs):
        # get user credentials
        usertype = getUserType(self.DBC)
        with self.DBC as sqlcnx:
            # if user is logged-in
            if usertype is not None:
                # create an SQL cursor to the database
                cur = sqlcnx.cursor(buffered=True, dictionary=True)
                # if user is an admin or dev, without specific record_id
                if (usertype[1] == 1 or usertype[1] == 2) and (record_id is None):
                    # if no record_id is indicated in the URL
                    # (display list of all records)
                    # fetch all columns from all rows in AffiliationRecordsTable
                    if (len(q) == 0):
                        cur.execute(
                            "SELECT clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                            "FROM AffiliationRecordsTable")
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
                            "LOWER(adviserName) LIKE %(query)s",
                            {"query": "%" + q + "%"})
                    data_list = cur.fetchall()
                    # close database cursor
                    cur.close()
                    # returns Mako-rendered view page HTML
                    # (control ViewAffiliationRecordList)
                    return self.renderer.render("view.mako", {
                        "data": data_list,
                        "q": q,
                        "user": usertype
                    })
                # handle viewing only one record
                # if user is a club, or a dev/admin indicating specific record_id
                elif (usertype[1] == 0) or ((usertype[1] == 1 or usertype[1] == 2) and record_id is not None):
                    # logged-in club cannot view other record_id's
                    if usertype[1] == 0:
                        if record_id is not None:
                            raise cherrypy.HTTPRedirect("/view")
                        else:
                            record_id = usertype[0]
                        
                    # (control ViewAffiliationRecord)
                    # Handles /view/<record_id>/ (admin/dev) and /view/ (club)
                    # display details about the affiliation record
                    cur.execute(
                        "SELECT clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                        "FROM AffiliationRecordsTable "
                        "WHERE clubID = %(clubID)s", {"clubID": record_id})
                    res = cur.fetchall()
                    record_info = None
                    check_affiliations = True
                    if len(res) == 1:
                        record_info = res[0]
                    elif len(res) == 0:
                        cherrypy.log.error(
                            "Warning (ViewRecord.index): trying to access invalid record_id {}".format(record_id)
                        )
                        check_affiliations = False
                    else:
                        cherrypy.log.error(
                            "Error (ViewRecord.index): too many matches for record_id {}".format(record_id)
                        )
                        check_affiliations = False
                    affiliation_list = None
                    if check_affiliations:
                        cur.execute(
                            "SELECT affiliated, status, hasAffiliationForms, benefits, remarks, schoolYear, yearsAffiliated, SCA, SCM, paymentMode, paymentDate, paymentID, paymentAmount, receiptNumber, paymentSendMode "
                            "FROM AffiliationTable "
                            "WHERE AffiliationRecordsTable_clubID = %(clubID)s", {"clubID": record_id})
                        affiliation_list = cur.fetchall()
                    cur.close()
                    return self.renderer.render(
                        "record.mako", {
                            "record_info": record_info,
                            "affiliations": affiliation_list,
                            "user": usertype,
                            "q": q
                        })
            # if user is not logged-in
            else:
                # go to login page
                raise cherrypy.HTTPRedirect("/login")
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })
