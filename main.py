# Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/02/06 (Simon) - Initial working code and documentation
# 2019/02/08 (Simon) - Updated CherryPy config, added getContent()
# 2019/02/13 (Simon) - Added Mako for rendering dynamic content, renamed getContent to renderContent
# 2019/02/19 (Simon) - Renamed class AffiliationDB to Root
#                    - Removed classes AffiliationRecord and Affiliation: all handled by class ViewRecord
#                        - URL scheme changed from /view/r/<r>/a/<a> to /view/<r>/<a>
# 2019/02/20 (Simon) - Updated documentation
#                    - Fixed templatelookup for caching locally
#                    - Added class DBConnection for handling a single persistent SQL database connection
#                    - Added atexit handler to disconnect from SQL database
#                    - Connecting to the database retries 3 times by default
# 2019/03/06 (Simon) - Added InputValidator and ContentRenderer helper classes
#                    - Added error logging to separate file
# 2019/03/07 (Simon) - Added class ViewApplication for handling /applications
# 2019/03/13 (Simon) - Methods approve+reject+view implemented in ViewApplication
#                    - Split affiliation input validation in AddRecord.insert() to be used by other methods
#                    - Program reads db.conf for the SQL server settings by default
# 2019/03/15 (Simon) - Started implementing Summary class for database summary
# 2019/03/22 (Simon) - Moved helper classes & methods to modules/_helpers.py
#                    - Moved CherryPy-exposed classes to individual files in modules/

import os  # for resolving filesystem paths
import atexit  # for handling server exit condition

from modules import Root  # import CherryPy-exposed Root class
import modules._helpers as helper  # import helper classes

# configuration of CherryPy webserver
if __name__ == '__main__':
    print("Running server")
    helper.cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'log.screen': False,
        'log.error_file': 'error.log',
        'log.access_file': 'access.log',
        'tools.gzip.on': True
    })

    # initialize persistent renderer & validator classes
    renderer = helper.ContentRenderer()
    validator = helper.InputValidator()

    # start a persistent connection to the SQL database
    dbc = helper.DBConnection("db.conf")
    dbc.connect()

    # disconnect from SQL database on exit
    atexit.register(lambda d: d.disconnect(), dbc)

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        },
        '/styles': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './styles'
        },
        '/scripts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './scripts'
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath("static/favicon.ico")
        }
    }
    # start the webserver
    helper.cherrypy.quickstart(Root(dbc, renderer, validator), '/', conf)
    print("\nServer exited")
