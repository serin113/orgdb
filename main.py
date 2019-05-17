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
# 2019/05/06 (Simon) - Added command line args for changing program options (listed in `main.py -h`)
# 2019/05/15 (Simon) - Fixed incorrect bytes() call when displaying an error message
#                    - Uses self-signed certs for running server through HTTPS locally (not for deployment)
#                    - Enforce HTTPS (HSTS), hide server version from HTTP header (for deployment)
# 2019/05/17 (Simon) - Added HTTP caching headers
#                    - System timezone printed as a debug message on startup
#                    - Added more CSP directives, http requests redirect to https, HSTS default
#                    - Disabled unused sessions feature

import os  # for resolving filesystem paths
import sys # for fetching system info (debugging & arguments)
import cherrypy  # import CherryPy library

import modules._helpers as helper  # import helper classes
from modules import Root  # import CherryPy-exposed Root class

from datetime import datetime, timedelta

def main(debug=None, clearlogs=None, reload=None, output=None, output_file=None):
    ON_HEROKU = os.environ.get('DYNO') is not None
    print("Running on Heroku: {}".format(ON_HEROKU))
    
    if debug is None:
        debug = True
    if clearlogs is None:
        clearlogs = True
    if reload is None:
        reload = False
    if output is None:
        output = True
    if output_file is None:
        output_file = False

    # configuration of CherryPy webserver
    if debug:
        delta = datetime.utcnow().astimezone().tzinfo.utcoffset(None)
        sign = "+" if delta >= timedelta(0) else "-"
        print("System timezone: UTC{}{}".format(sign, delta))
        print("Debug messages enabled")
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
            "default-src 'none';"
            "style-src 'self';"
            "font-src 'self' data: https://fonts.gstatic.com;"
            "img-src 'self' data:;"
            "script-src 'self';"
            "frame-ancestors 'none';"
            "base-uri 'self';"
            "form-action 'self'")
        headers['Strict-Transport-Security'] = 'max-age=31536000'
        headers["Referrer-Policy"] = 'same-origin'
        headers["X-Content-Type-Options"] = 'nosniff'
            
    @cherrypy.tools.register('before_finalize', priority=61)
    def staticcacheheaders():
        headers = cherrypy.response.headers
        headers['Cache-Control'] = 'public, max-age=31536000'
        headers['Expires'] = (datetime.utcnow()+timedelta(seconds=31536000)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    @cherrypy.tools.register('before_handler', priority=50)    
    def check_ssl():
        direct_http = False
        forward_http = False
        # if received request is in http
        if cherrypy.request.scheme == "http":
            direct_http = True
        # if request was forwarded
        if "X-Forwarded-Proto" in cherrypy.request.headers.keys():
            # if original request is in http
            if cherrypy.request.headers["X-Forwarded-Proto"] == "http":
                forward_http = True
        if direct_http or forward_http:
            # redirect requesting user to https
            raise cherrypy.HTTPRedirect(cherrypy.url().replace("http:", "https:"),
                                    status=301)

    def handle_error():
        cherrypy.response.status = 500
        cherrypy.log.error(cherrypy._cperror.format_exc())
        html = renderer.render("dialog.mako", {'title': "An error occured."})
        cherrypy.response.body = [bytes(html, "utf8")]

    def error_page_404(status, message, traceback, version):
        from modules.Login import getUserType  # for fetching current logged-in user for template
        return renderer.render(
            "404.mako", {'user': getUserType(helper.DBConnection("db.conf"))})

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'response.headers.server': 'OrgDB',
        'log.screen': output,
        'log.error_file': 'error.log' if output_file else "",
        'log.access_file': 'access.log' if output_file else "",
        'error_page.404': error_page_404,
        'request.error_response': handle_error,
        'request.show_tracebacks': debug,
        'engine.autoreload.on': reload,
        'tools.check_ssl.on': True
    })
    if ON_HEROKU:
        cherrypy.config.update({
            'server.socket_port': int(os.environ.get('PORT'))
        })
    else:
        cherrypy.config.update({
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': 'cert.pem',
            'server.ssl_private_key': 'privkey.pem',
        })
    
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.secureheaders.on': True
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static',
            'tools.staticcacheheaders.on': True
        },
        '/styles': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './styles',
            'tools.staticcacheheaders.on': True
        },
        '/scripts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './scripts',
            'tools.staticcacheheaders.on': True
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath("static/favicon.ico"),
            'tools.staticcacheheaders.on': True
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
    from optparse import OptionParser # for parsing arguments
    parser = OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Show debug messages", default=False)
    parser.add_option("-x", "--clearlogs", action="store_true", dest="clearlogs", help="Clear previous logs on execute", default=False)
    parser.add_option("-r", "--reload", action="store_true", dest="reload", help="Reload webserver on code changes", default=False)
    parser.add_option("-o", "--output", action="store_true", dest="output", help="Output debug messages to stdout", default=False)
    parser.add_option("-f", "--outtofile", action="store_true", dest="output_file", help="Output debug & access messages to debug.log & access.log", default=False)
    (options, args) = parser.parse_args(sys.argv[1:])
    main(**vars(options))
