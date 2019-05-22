#!/usr/bin/env python3

import modules
import os
import mysql.connector

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
    
    test = open("db.conf", "r")
    print(test.read())
    test.close()
    print("Creating database connection")
    # create database connection
    dbc = modules.DBConnection("db.conf")

    with dbc as sqlcnx:
        cur = sqlcnx.cursor()
        f = open("db.sql", "r")
        sqlfile = f.read()
        f.close()
        commands = sqlfile.split(";")
        for command in commands:
            try:
                cur.execute(command)
            except mysql.connector.errors.OperationalError as msg:
                print("[Command skipped] ", msg)