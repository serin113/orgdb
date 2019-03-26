# NOTE: DO NOT USE THIS IN PRODUCTION

import modules

dbc = modules.DBConnection("db.conf")

modules.createCredentials("club", "club", 0, dbc)
modules.createCredentials("club2", "club2", 0, dbc)
modules.createCredentials("admin", "psysc", 1, dbc)
modules.createCredentials("dev", "cs192", 2, dbc)