# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
#                    - Uses a dictionary for passing data to the template
# 2019/03/23 (Simon) - Added (int) overallTotal to data sent to template
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
#                    - Added Login.accessible_by decorators to limit page access to specific users

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /summary
class Summary(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()

    @cherrypy.expose
    @accessible_by("admin")
    def index(self, q=None):
        sqlcnx = self.DBC.connect()  # connect to SQL database
        cur = sqlcnx.cursor(buffered=True)  # create SQL database cursor
        data = {}
        if q is None:
            # get school year range
            cur.execute(
                "SELECT MIN(schoolYear), MAX(schoolYear-1+yearsAffiliated) FROM AffiliationTable ORDER BY schoolYear"
            )
            res = cur.fetchall()

            if len(res) > 0:
                if res[0][0] is not None or res[0][1] is not None:
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
                else:
                    data = None
            else:
                data = None
        else:
            # handle case for filtering summary results accdg. to query
            pass
        cur.close()
        return self.renderer.render("summary.mako", {
            "data": data,
            'user': getUserType(self.DBC)
        })  # display summary data