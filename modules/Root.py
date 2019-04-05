# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file
# 2019/03/26 (Simon) - Login.getUserType values passed to ContentRenderer.render
# 2019/03/29 (Simon) - "DBC" argument now indicates the database configuration settings
#                           instead of a DBConnection class
# 2019/04/02 (Simon) - Added /edit, changed "back" URL for debug dialog
# 2019/04/05 (Simon) - Removed persistent InputValidator class from handler classes

from ._helpers import *
from .AddApplication import *
from .AddRecord import *
from .EditRecord import *
from .Login import *
from .Summary import *
from .ViewApplication import *
from .ViewRecord import *


# class used by CherryPy to handle HTTP requests for /
class Root(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        if DBC is not None:
            self.DBC = DBConnection(DBC)
        else:
            self.DBC = DBConnection("db.conf")
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()
        if Validator is not None:
            self.validator = Validator
        else:
            self.validator = InputValidator()

        # class handling /login
        self.login = Login(DBC=DBC, Renderer=Renderer)
        # class handling /apply
        self.apply = AddApplication(DBC=DBC, Renderer=Renderer)
        # class handling /view
        self.view = ViewRecord(DBC=DBC, Renderer=Renderer)
        # class handling /add
        self.add = AddRecord(DBC=DBC, Renderer=Renderer)
        # class handling /applications
        self.applications = ViewApplication(DBC=DBC, Renderer=Renderer)
        # class handling /summary
        self.summary = Summary(DBC=DBC, Renderer=Renderer)
        # class handling /edit
        self.edit = EditRecord(DBC=DBC, Renderer=Renderer)

    @cherrypy.expose
    @accessible_by("dev")
    def dialog(self):
        return self.renderer.render(
            "dialog.mako", {
                'user': getUserType(self.DBC),
                'title': "Title",
                'message': "Message Message Message!",
                'linkaddr': "#back",
                'linktext': "< Back"
            })

    @cherrypy.expose
    # CherryPy method handling /
    def index(self):
        # returns Mako-rendered homepage HTML
        return self.renderer.render("index.mako",
                                    {'user': getUserType(self.DBC)})

    @cherrypy.expose
    def logout(self):
        self.login.logout()
