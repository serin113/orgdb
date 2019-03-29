# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
#                    - Uses a dictionary for passing data to the template
# 2019/03/23 (Simon) - Added (int) overallTotal to data sent to template
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users
# 2019/03/27 (Simon) - Added filtering functionality
# 2019/03/29 (Simon) - "DBC" argument now indicates the database configuration settings
#                           instead of a DBConnection class
#                    - Database connection now handled using a with statement

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /summary
class Summary(object):
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
    @accessible_by("admin")
    def index(self, q=""):
        data = None
        with self.DBC as sqlcnx:
            cur = sqlcnx.cursor(buffered=True)  # create SQL database cursor
            if (len(q) == 0):
                # get school year range
                cur.execute(
                    "SELECT MIN(schoolYear), MAX(schoolYear-1+yearsAffiliated) FROM AffiliationTable ORDER BY schoolYear"
                )
                res = cur.fetchall()
            else:
                # create year range (q to q+1)
                qi = toInt(q)
                if qi:
                    if qi in range(2007, 2051):
                        res = [(qi, qi + 1)]
                else:
                    res = []

            if len(res) > 0:
                if res[0][0] is not None or res[0][1] is not None:
                    data = {}
                    # for every year within the range
                    for year in range(res[0][0], res[0][1] + 1):
                        region_total = defaultdict(lambda: 0)
                        level_total = defaultdict(lambda: 0)
                        type_total = defaultdict(lambda: 0)
                        # fetch all affiliated clubs for a specific year
                        cur.execute(
                            "SELECT region, level, type "
                            "FROM (AffiliationRecordsTable INNER JOIN AffiliationTable ON AffiliationRecordsTable.clubID = AffiliationTable.AffiliationRecordsTable_clubID)"
                            "WHERE %(schoolYear)s BETWEEN schoolYear AND schoolYear-1+yearsAffiliated "
                            "AND affiliated = 1 ", {"schoolYear": year})
                        res = cur.fetchall()
                        # count totals per region/level/type
                        for record in res:
                            region_total[record[0]] += 1
                            level_total[record[1]] += 1
                            type_total[record[2]] += 1
                        overall_total = len(res)
                        # save data for specific year
                        data[year] = (region_total, level_total, type_total,
                                      overall_total)
            cur.close()
            return self.renderer.render("summary.mako", {
                "data": data,
                'user': getUserType(self.DBC),
                'q': q
            })  # display summary data
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.<br>",
                'linkaddr': "javascript:history.back();",
                'linktext': "&gt; Back",
                'user': getUserType(self.DBC)
            })
