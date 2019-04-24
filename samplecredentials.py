#!/usr/bin/env python3

# NOTE: DO NOT USE THIS IN PRODUCTION

import modules

print("Updating config")
# update cherrypy global config
modules.cherrypy.config.update({
    'log.screen': False,
    'log.error_file': "credentials_error.log",
    'log.access_file': "",
    'request.show_tracebacks': True,
    'engine.autoreload.on': False
})

print("Creating database connection")
# create database connection
dbc = modules.DBConnection("db.conf")

print("Inserting record")
# insert sample record
add = modules.AddRecord(DBC="db.conf")._insert(
    "1", "1", "1", "School", "Club Name", "Address", "City", "Province",
    "Adviser Name", "Contact", "email@edu.ph", "1", "", "1", "", "", "2018",
    "2", "1", "50", "", "2019-01-01", "", "20000", "", "")

print("Creating credentials")
# create sample admin & dev accounts
creds = [("admin", "psysc", 1), ("dev", "cs192", 2)]
# print sample accounts
for c in creds:
    modules.createCredentials(c[0], c[1], c[2], dbc)
    print("\t[{2}] \"{0}\": \"{1}\"".format(c[0], c[1], c[2]))
