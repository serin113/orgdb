# Created in 2019-03-22 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/22 (Simon) - Moved class to this file

from ._helpers import *
from .Summary import *
from .ViewApplication import *
from .ViewRecord import *
from .AddApplication import *
from .AddRecord import *


# class used by CherryPy to handle HTTP requests for /
class Root(object):
    def __init__(self, DBC=None, Renderer=None, Validator=None):
        self.renderer = Renderer
        # class handling /view
        self.view = ViewRecord(DBC=DBC, Renderer=Renderer)
        # class handling /add
        self.add = AddRecord(DBC=DBC, Renderer=Renderer, Validator=Validator)
        # class handling /apply
        self.apply = AddApplication(
            DBC=DBC, Renderer=Renderer, Validator=Validator)
        # class handling /applications
        self.applications = ViewApplication(
            DBC=DBC, Renderer=Renderer, Validator=Validator)
        # class handling /summary
        self.summary = Summary(DBC=DBC, Renderer=Renderer)

    @cherrypy.expose
    # CherryPy method handling /
    def index(self):
        # returns Mako-rendered homepage HTML
        return self.renderer.render("index.mako")
