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

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /view
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
    # CherryPy method handling /view
    def index(self, q="", record_id=None, affiliation_id=None):
        with self.DBC as sqlcnx:
            # get user credentials
            usertype = getUserType(self.DBC)
            # if user is logged-in
            if usertype is not None:
                # if user is an admin or dev
                if usertype[1] == 1 or usertype[1] == 2:
                    # if no record_id is indicated in the URL
                    # (display list of all records)
                    # create an SQL cursor to the database
                    cur = sqlcnx.cursor(buffered=True)
                    if record_id is None:
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
                        res = cur.fetchall()
                        # close database cursor
                        cur.close()
                        self.DBC.disconnect()
                        # create (list of dicts) data_list from (list of tuples) res
                        data_list = []
                        for record in res:
                            record_dict = {
                                'clubID': record[0],
                                'dateUpdated': record[1],
                                'region': record[2],
                                'level': record[3],
                                'type': record[4],
                                'school': record[5],
                                'clubName': record[6],
                                'address': record[7],
                                'city': record[8],
                                'province': record[9],
                                'adviserName': record[10],
                                'contact': record[11],
                                'email': record[12]
                            }
                            data_list.append(record_dict)
                        # returns Mako-rendered view page HTML
                        # (control ViewAffiliationRecordList)
                        return self.renderer.render("view.mako", {
                            "data": data_list,
                            "q": q,
                            'user': usertype
                        })
                    # if record_id is indicated in the URL
                    # (display individual record)
                    else:
                        # (control ViewAffiliationRecord)
                        # Handles /view/<record_id>/
                        # display details about the affiliation record
                        cur.execute(
                            "SELECT clubID, dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                            "FROM AffiliationRecordsTable "
                            "WHERE clubID = %(clubID)s", {"clubID": record_id})
                        res = cur.fetchall()
                        cur.close()
                        self.DBC.disconnect()
                        record_info = None
                        if len(res) == 1:
                            record_info = {
                                "clubID": res[0][0],
                                "dateUpdated": res[0][1],
                                "region": res[0][2],
                                "level": res[0][3],
                                "type": res[0][4],
                                "school": res[0][5],
                                "clubName": res[0][6],
                                "address": res[0][7],
                                "city": res[0][8],
                                "province": res[0][9],
                                "adviserName": res[0][10],
                                "contact": res[0][11],
                                "email": res[0][12]
                            }
                        elif len(res) == 0:
                            # print("No match")
                            pass
                        else:
                            # print("too many matches")
                            pass
                        return self.renderer.render(
                            "record.mako", {
                                "record_info": record_info,
                                "affiliations": [],
                                'user': usertype
                            })
                # handle viewing only one record
                elif type == 0:
                    return self.renderer.render("record.mako", {
                        "record_info": None,
                        "affiliations": [],
                        'user': usertype
                    })
            # if user is not logged-in
            else:
                # go to login page
                raise cherrypy.HTTPRedirect("/login")
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.<br>",
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back",
                'user': getUserType(self.DBC)
            })
