# Created in 2019-03-21 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/21 (Simon) - Moved helper methods & classes from main.py to this file
# 2019/03/26 (Simon) - DBConnection.connect & ContentRenderer.render catches more exceptions
#                    - ContentRenderer.render caught exceptions only shown if debug=True
#                    - Updated newID

from collections import defaultdict  # for general-purpose dicts with default values
import mysql.connector  # for handling MySQL database connections
import cherrypy  # for handling HTTP requests
from mako.lookup import TemplateLookup  # for template rendering
import mako.exceptions
from datetime import date, datetime  # for getting the current date
import re  # for input validation
from uuid import uuid4  # for creating a unique ID
from hashlib import sha512  # for creating a unique ID from other data

#
# HELPER METHODS
#


# returns a string-type unique id from string_base
def newID(string_base=None, length=None, prefix=None, postfix=None):
    if string_base is not None:
        string = sha512(bytes(string_base, "utf8")).hexdigest()
        if length is not None:
            string = string[:length]
        if prefix is not None:
            string = prefix + string
        if postfix is not None:
            string = string + postfix
        return string
    return str(uuid4())


# returns an integer if the input string s
# is a valid integer, returns False otherwise;
# used for input validation of int-type inputs
# parameters:
#   (string type) s
def toInt(s):
    try:
        int(s)
    except:
        return False
    return int(s)


# get the current date, optionally excluding the time
# parameters:
#   (boolean type) hasTime
def today(hasTime=True):
    if hasTime:
        return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return (datetime.now().strftime("%Y-%m-%d"))


#
# HELPER CLASSES
#


# class handling a single persistent SQL database connection
# class parameters:
#   (dict type) config      - SQL database configuration
# methods:
#   connect(retries=0)     - connects to an SQL database using the config
#   disconnect()           - disconnects previous connection, if any
class DBConnection(object):
    def __init__(self, arg=None):
        self.connection = None
        # default configuration for connecting to a MySQL server
        if arg is None:
            self.config = {
                'user': 'cs192',
                'password': 'cs192',
                'host': '127.0.0.1',
                'database': 'mydb',
                'raise_on_warnings': True
            }
        # use the passed config if given
        else:
            self.config = arg

    # for checking if there is still a connection to the database
    # returns True if connected, False otherwise
    def is_connected(self):
        if self.connection is None:
            return False
        return self.connection.is_connected()

    # handles connecting to the database
    # returns the connection object, or None if it failed to connect
    def connect(self, retries=3):
        # try connecting to the SQL server if not yet connected, handling any exceptions
        ctr = 0
        # keep trying to connect
        while (self.connection is None) and (ctr <= retries):
            try:
                self.connection = mysql.connector.connect(
                    option_files=self.config)
                if self.is_connected():
                    # return object for interacting with the SQL database
                    cherrypy.log.error("Connected to SQL database")
                    return self.connection
            except mysql.connector.Error as err:
                if ctr == retries:
                    # unreachable server
                    if err.errno == mysql.connector.errorcode.CR_CONN_HOST_ERROR:
                        cherrypy.log.error(
                            "Error (DBConnection.connect): SQL server is unreachable (2003)"
                        )
                    # wrong database user+password
                    elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                        cherrypy.log.error(
                            "Error (DBConnection.connect): Something is wrong with your user name or password (1045)"
                        )
                    # non-existent database
                    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                        cherrypy.log.error(
                            "Error (DBConnection.connect): Database does not exist (1049)"
                        )
                    # everything else
                    else:
                        cherrypy.log.error("Error (DBConnection.connect): " +
                                           str(err) + " (" + err.errno + ")")
                self.connection = None
                ctr += 1
        # check if previous SQL connection is still connected
        if self.connection is not None:
            if self.connection.is_connected():
                # return object for interacting with the SQL database
                return self.connection
        # only executes if not yet connected for the first time
        cherrypy.log.error(
            "Error (DBConnection.connect): Cannot connect to SQL database")
        return None

    # disconnects from the database
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
        cherrypy.log.error("Disconnected from SQL database")
        return


# class handling input validation
# class parameters:
#   None
# methods:
#   setLimits(fields): set limits for input validator
#   (dict/str/None) fields  - which input fields to validate
#                   * (if dict type)
#                       - key: (str type) input field name
#                       - value: (tuple type) limits
#                           - 0: field minimum (inclusive)
#                           - 1: field maximum (inclusive)
#                           - 2: is the field required?
#                   * (if str type) valid preset strings:
#                       - "record", "affiliation", "application", "application_renew"
#   validate(inputs,skip=[])    - validate inputs, while skipping any key in list
#                               - expects:
#                                   - (dict) inputs: key:<name>, value:<field value>
#                                   - (list) skip: <name>
class InputValidator(object):
    # preset input field limits
    record_dict = {
        'region': (1, 17, True),
        'level': (1, 4, True),
        'type': (1, 3, True),
        'school': (2, 100, True),
        'clubName': (2, 100, True),
        'address': (2, 200, True),
        'city': (2, 45, True),
        'province': (2, 45, True),
        'adviserName': (1, 100, True),
        'contact': (4, 45, True),
        'email': (0, 45, True)
    }
    affiliation_dict = {
        'affiliated': (0, 1, True),
        'status': (0, 45, False),
        'hasAffiliationForms': (0, 1, True),
        'benefits': (0, 200, False),
        'remarks': (0, 200, False),
        'schoolYear': (2007, 2050, True),
        'yearsAffiliated': (1, 50, True),
        'SCA': (1, 32767, True),
        'SCM': (1, 32767, True),
        'paymentMode': (0, 200, False),
        'paymentID': (0, 200, False),
        'paymentAmount': (0, 1000000000, False),
        'receiptNumber': (0, 200, False),
        'paymentSendMode': (0, 200, False)
    }
    application_dict = {'hasRecord': (0, 1, False)}

    def __init__(self):
        self.setLimits()

    def setLimits(self, arg=None):
        self.limits = defaultdict(lambda: None)
        # checking if using preset or custom limits
        if arg is None:
            self.limits.update({
                **self.record_dict,
                **self.affiliation_dict,
                **self.application_dict
            })
        elif type(arg) is str:
            if arg is "record":
                self.limits.update({
                    **self.record_dict,
                    **self.affiliation_dict
                })
            elif arg is "affiliation":
                self.limits.update({**self.affiliation_dict})
            elif arg is "application":
                self.limits.update({
                    **self.record_dict,
                    **self.affiliation_dict,
                    **self.application_dict
                })
            elif arg is "application_renew":
                self.limits.update({
                    **self.affiliation_dict,
                    **self.application_dict
                })
        else:
            self.limits.update(arg)

    # for validating dict-type object "inputs"
    # returns a list of errors (empty list if none)
    # each error is a tuple (error_message, field_name, field_value)
    def validate(self, inputs, skip=[]):
        errors = []
        if self.limits is None:
            return errors
        # iterate through the "inputs" dict
        for key, val in inputs.items():
            if key in skip:
                continue
            # skip item if it doesn't have defined limits
            if self.limits[key] is None:
                continue
            # get limits
            min, max, required = self.limits[key]
            # check if item is None or an empty string
            isMissing = False
            if required:
                if val is None:
                    errors.append(("Missing input", key, val))
                    isMissing = True
                elif type(val) is str:
                    if len(val) == 0:
                        errors.append(("Missing input", key, val))
                        isMissing = True
            # check if item is within limits
            if type(val) is int and not isMissing:
                if not (min <= val <= max):
                    errors.append(("Invalid length", key, val))
            elif type(val) is str and not isMissing:
                if not (min <= len(val) <= max):
                    errors.append(("Invalid length", key, val))
            # if current field item is "email", check if it has a valid format
            if key is "email" and not isMissing:
                email_pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
                email_match = re.match(email_pattern, val, re.M)
                if not email_match:
                    errors.append(("Invalid email address", key, val))
            # if current field item is "paymentDate", check if it has a valid format and is a valid past date
            elif key is "paymentDate" and not isMissing:
                # date comparison assumes ISO format: yyyy-mm-dd
                date_pattern = r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
                date_match = re.match(date_pattern, val, re.M)
                if not date_match:
                    errors.append(("Invalid date (format is )", key, val))
                if (str(val) > str(today(hasTime=False))):
                    errors.append(("date_future", key, val))
        return errors


# persistent class handling Mako template rendering
# class parameters:
#   None
# methods:
#   render(templatefile, templatevars=None): return rendered HTML
#       (string type) templatefile (required) - name of template file
#       (dict type) templatevars - dict of variables ("name":"value") to pass to Mako
class ContentRenderer(object):
    def __init__(self, debug=None):
        if debug is None:
            self.debug = False
        else:
            self.debug = debug
        self.lookup = TemplateLookup(
            directories=["templates/"],
            collection_size=100,
            format_exceptions=True,
            module_directory="tmp/mako_modules")

    def render(self, templatefile, templatevars=None):
        try:
            t = self.lookup.get_template(templatefile)
            if (templatevars is None):
                return t.render()
            return t.render(**templatevars)
        except mako.exceptions.MakoException as err:
            cherrypy.log.error("Error (ContentRenderer.render): " + str(err))
            if self.debug:
                return str(err)
            return "<html><body>Sorry, an error occured</body></html>"
