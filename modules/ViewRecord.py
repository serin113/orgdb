# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon)- Moved class to this file

from ._helpers import *


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
            sqlcnx = self.DBC.connect()  # connect to SQL server
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database
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
                "q": q
            })

        else:
            # (control ViewAffiliationRecord)

            if affiliation_id is None:
                # Handles /view/<record_id>/
                # should return details about the affiliation record
                return "record id: %s" % record_id
            else:
                # Handles /view/<record_id>/<affiliation_id>
                # should return details about a specific affiliation within a club's record
                return "record id: %s<br>affiliation id: %s" % (record_id,
                                                                affiliation_id)
