#!/usr/bin/env python3
# NOTE: DO NOT USE THIS IN PRODUCTION

import modules

print("Updating config")
modules.cherrypy.config.update({
    'log.screen': False,
    'log.error_file': "credentials_error.log",
    'log.access_file': "",
    'request.show_tracebacks': True,
    'engine.autoreload.on': False
})

print("Creating database connection")
dbc = modules.DBConnection("db.conf")

print("Inserting record")
add = modules.AddRecord(DBC="db.conf")._insert(
    "1", "1", "1", "School", "Club Name", "Address", "City", "Province",
    "Adviser Name", "Contact", "email@edu.ph", "1", "", "1", "", "", "2018",
    "2", "1", "50", "", "2019-01-01", "", "20000", "", "")
clubid = modules.newID(
    "1" + "1" + "1" + "School" + "Club Name" + "Address" + "City" + "Province"
    + "Adviser Name" + "Contact" + "email@edu.ph",
    length=8)

print("Creating credentials")
creds = [(clubid, clubid, 0), ("admin", "psysc", 1), ("dev", "cs192", 2)]
for c in creds:
    modules.createCredentials(c[0], c[1], c[2], dbc)
    print("\t[{2}] \"{0}\": \"{1}\"".format(c[0], c[1], c[2]))
