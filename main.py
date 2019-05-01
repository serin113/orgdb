#!/usr/bin/env python3

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
# 2019/03/26 (Simon) - Added debug & clearLogs boolean options
#                    - Added error handling
# 2019/03/29 (Simon) - Fixed handle_error not displaying an error page
#                    - Removed persistent DBConnection (classes create a new one instead)
#                    - Added debug options
#                    - Webserver now open to localhost & LAN
# 2019/04/02 (Simon) - Added HTTP secure headers, added 404 error handling
# 2019/04/05 (Simon) - Fixed typo
#                    - Removed persistent InputValidator class passed to Root
# 2019/04/23 (Simon) - Moved actions to main() method
#                    - Print Python version if debug messages are enabled
#                    - Error handler now uses Mako template
# 2019/04/29 (Simon) - Python, CherryPy, & Mako module versions printed as debug messages

import os  # for resolving filesystem paths

import cherrypy  # import CherryPy library

import modules._helpers as helper  # import helper classes
from modules import Root  # import CherryPy-exposed Root class

def main(debug=None, clearlogs=None, reload=None):
    ON_HEROKU = os.environ.get('DYNO') is not None
    print("Running on Heroku: {}".format(ON_HEROKU))
    
    if debug is None:
        debug = True
    if clearlogs is None:
        clearlogs = True
    if reload is None:
        reload = True

    # configuration of CherryPy webserver
    if debug:
        print("Debug messages enabled")
        import sys
        print("Python version: {}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        print("CherryPy version: ", cherrypy.__version__)
        import mako
        print("Mako version: ", mako.__version__)
    if clearlogs:
        try:
            os.remove("access.log")
        except:
            pass
        try:
            os.remove("error.log")
        except:
            pass

    # initialize persistent renderer
    renderer = helper.ContentRenderer(debug=debug)

    @cherrypy.tools.register('before_finalize', priority=60)
    def secureheaders():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        headers['Content-Security-Policy'] = (
            "default-src 'self';"
            "style-src 'self' 'unsafe-inline';"
            "font-src 'self' data: https://fonts.gstatic.com;"
            "img-src 'self' data:;"
            "script-src 'self'")

    def handle_error():
        cherrypy.response.status = 500
        cherrypy.log.error(cherrypy._cperror.format_exc())
        html = renderer.render("dialog.mako", {'title': "An error occured."})
        cherrypy.response.body = [bytes(html)]

    def error_page_404(status, message, traceback, version):
        from modules.Login import getUserType  # for fetching current logged-in user for template
        return renderer.render(
            "404.mako", {'user': getUserType(helper.DBConnection("db.conf"))})

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'log.screen': False,
        'log.error_file': 'error.log' if debug else "",
        'log.access_file': 'access.log' if debug else "",
        'error_page.404': error_page_404,
        'request.error_response': handle_error,
        'request.show_tracebacks': debug,
        'engine.autoreload.on': reload
    })
    if ON_HEROKU:
        cherrypy.config.update({
            'server.socket_port': int(os.environ.get('PORT'))
        })

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.secureheaders.on': True
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
    print("Running server")
    if ON_HEROKU:
        import urllib.parse
        urllib.parse.uses_netloc.append("mysql")
        urlstr = os.environ.get('CLEARDB_DATABASE_URL')
        url = urllib.parse.urlparse(urlstr)
        db_conf = open("db.conf", "w")
        db_conf.write("[connector_python]\n")
        db_conf.write("host = {}\ndatabase = {}\nuser = {}\npassword = {}\nport = {}\nraise_on_warnings = True\n".format(url.hostname, url.path[1:], url.username, url.password, 3306))
        db_conf.close()
    cherrypy.quickstart(Root("db.conf", Renderer=renderer), '/', conf)
    print("\nServer exited")

if __name__ == '__main__':
    main()