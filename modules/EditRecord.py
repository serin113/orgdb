# Created in 2019-04-01 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/04/01 (Simon) - Initial code
# 2019/04/05 (Simon) - Removed duplicate checking in update()
# 2019/05/15 (Simon) - Added **kwargs to CherryPy-exposed methods to catch unexpected parameters w/o an error
#                    - index() passes "q" parameter through template

from ._helpers import *
from .Login import *


# class used by CherryPy for handling /edit/<record_id>
@cherrypy.popargs('record_id')
class EditRecord(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBConnection(DBC)
        else:
            self.DBC = DBConnection("db.conf")
        if Validator is not None:
            self.validator = Validator
        else:
            self.validator = InputValidator()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()

    @cherrypy.expose
    @accessible_by("admin")
    # CherryPy method handling /edit/<record_id>
    def index(self, q="", record_id=None, **kwargs):
        with self.DBC as sqlcnx:
            # create database cursor
            cur = sqlcnx.cursor(buffered=True)
            # fetch club info
            cur.execute(
                "SELECT dateUpdated, region, level, type, school, clubName, address, city, province, adviserName, contact, email "
                "FROM AffiliationRecordsTable "
                "WHERE clubID = %(clubID)s", {"clubID": record_id})
            # if exactly one matching club
            if cur.rowcount == 1:
                # pass club info to template
                res = cur.fetchall()
                record_info = {
                    'dateUpdated': res[0][0],
                    'region': res[0][1],
                    'level': res[0][2],
                    'type': res[0][3],
                    'school': res[0][4],
                    'clubName': res[0][5],
                    'address': res[0][6],
                    'city': res[0][7],
                    'province': res[0][8],
                    'adviserName': res[0][9],
                    'contact': res[0][10],
                    'email': res[0][11]
                }
                # returns Mako-rendered edit page HTML
                return self.renderer.render("edit.mako", {
                    'user': getUserType(self.DBC),
                    'record_info': record_info,
                    'q': q
                })
            # if != 1 matching club
            else:
                # log if more than 1 club with same ID
                if cur.rowcount > 1:
                    cherrypy.log.error(
                        "Error (EditRecord.index): More than one club with same ID: "
                        + clubid)
                # display error
                return self.renderer.render(
                    "dialog.mako", {
                        'title': "Error!",
                        'message': "Cannot edit non-existent club.",
                        'linkaddr': "#back",
                        'linktext': "< Back",
                        'user': getUserType(self.DBC)
                    })
        # display error
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })

    @cherrypy.expose
    @accessible_by("admin")
    # CherryPy method handling /edit/<record_id>/update with incoming POST/GET data
    # every argument in the method (except for self) is defined in db.sql
    def update(self,
               record_id=None,
               region=None,
               level=None,
               type=None,
               school=None,
               clubname=None,
               address=None,
               city=None,
               province=None,
               advisername=None,
               contact=None,
               email=None,
               **kwargs):
        # if no clubID (record_id) specified, log error and go back
        if record_id is None:
            cherrypy.log.error("Error (EditRecord.update): Missing club ID: " +
                               record_id)
            raise cherrypy.HTTPRedirect("/edit")
        with self.DBC as sqlcnx:
            # string format for updating record_data in SQL database
            # table structure is defined in db.sql
            update_record = ("UPDATE AffiliationRecordsTable SET "
                             "dateUpdated = %(dateUpdated)s, "
                             "region = %(region)s, "
                             "level = %(level)s, "
                             "type = %(type)s, "
                             "school = %(school)s, "
                             "clubName = %(clubName)s, "
                             "address = %(address)s, "
                             "city = %(city)s, "
                             "province = %(province)s, "
                             "adviserName = %(adviserName)s, "
                             "contact = %(contact)s, "
                             "email = %(email)s "
                             "WHERE clubID = %(clubID)s")
            cur = sqlcnx.cursor(
                buffered=True)  # create an SQL cursor to the database

            # check if clubID to be updated matches exactly 1 club
            cur.execute(
                "SELECT clubID FROM AffiliationRecordsTable "
                "WHERE clubID = %(clubID)s", {"clubID": record_id})
            res = cur.fetchall()

            # log if no matching clubID
            if len(res) == 0:
                cherrypy.log.error(
                    "Error (EditRecord.update): Tried to edit nonexistent club ID: "
                    + clubid)
                raise cherrypy.HTTPRedirect("/edit")
            # log if more than 1 club with same ID
            elif len(res) > 1:
                cherrypy.log.error(
                    "Error (EditRecord.update): More than one club with same ID: "
                    + clubid)
                raise cherrypy.HTTPRedirect("/edit")
            # prepare updated data
            date_today = today()
            record_data = {
                'clubID': record_id,
                'dateUpdated': date_today,
                'region': toInt(region),
                'level': toInt(level),
                'type': toInt(type),
                'school': school,
                'clubName': clubname,
                'address': address,
                'city': city,
                'province': province,
                'adviserName': advisername,
                'contact': contact,
                'email': email
            }
            # input validation
            self.validator.setLimits("record")
            errors = self.validator.validate(record_data)
            # display errors, if any
            if len(errors) > 0:
                cur.close()  # close database cursor
                return self.renderer.render(
                    "dialog.mako", {
                        'title': "Error!",
                        'message':
                        "Invalid affiliation record data:<br>" + errortext,
                        'linkaddr': "#back",
                        'linktext': "< Back",
                        'errors': errors,
                        'user': getUserType(self.DBC)
                    })
            cur.execute(update_record,
                        record_data)  # insert record_data to database
            sqlcnx.commit()  # commit changes to database
            cur.close()  # close database cursor
            # display update success HTML
            return self.renderer.render(
                "dialog.mako", {
                    'title': "Affiliation record updated.",
                    'linkaddr': "/view/" + record_id,
                    'linktext': " Go to record",
                    'user': getUserType(self.DBC)
                })
        # display error
        return self.renderer.render(
            "dialog.mako", {
                'title': "Error!",
                'message': "A database error occured.",
                'linkaddr': "#back",
                'linktext': "< Back",
                'user': getUserType(self.DBC)
            })
