#!/usr/bin/env python3

import modules
import os

print("Updating config")
# update cherrypy global config
modules.cherrypy.config.update({
    'log.screen': False,
    'log.error_file': "credentials_error.log",
    'log.access_file': "",
    'request.show_tracebacks': True,
    'engine.autoreload.on': False
})

if os.environ.get('DYNO') is not None:
    print("Creating db.conf from Heroku environment vars")
    import urllib.parse
    urllib.parse.uses_netloc.append("mysql")
    urlstr = os.environ.get('CLEARDB_DATABASE_URL')
    print(urlstr)
    url = urllib.parse.urlparse(urlstr)
    db_conf = open("db.conf", "w")
    db_conf.write("[connector_python]\n")
    db_conf.write("host = {}\ndatabase = {}\nuser = {}\npassword = {}\nport = {}\nraise_on_warnings = True\n".format(url.hostname, url.path[1:], url.username, url.password, 3306))
    db_conf.close()

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

# create admin & dev accounts
creds = []
pass1 = input("Password for admin (enter to skip): ")
if len(pass1) > 0:
    creds.append(("admin", pass1, 1))
pass2 = input("Password for dev (enter to skip): ")
if len(pass2) > 0:
    creds.append(("dev", pass2, 2))
for c in creds:
    modules.createCredentials(c[0], c[1], c[2], dbc)
    #print("\t[{2}] \"{0}\": \"{1}\"".format(c[0], c[1], c[2]))
