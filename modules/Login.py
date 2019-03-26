# Created in 2019-03-23 for PSYSC as part of a system for managing science club affiliations.

# Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
# Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

# Code History:
# 2019/03/23 (Simon) - Initial login code
# 2019/03/26 (Simon) - Added helper functions accessible_by & getUserType

from ._helpers import *
from os import urandom
from hashlib import pbkdf2_hmac
from functools import wraps


# (decorator to be used in CherryPy page handler methods)
# causes a redirect to the homepage if user is not
# in authorized usertypes
# usertypes:
#   (string type) "default"(logged-out), "club"(club), "admin"(admin)
#   or (list type) [list of strings]
def accessible_by(usertype):
    def wrap(func):
        @wraps(func)
        def func_wrap(*args, **kwargs):
            # args[0] is usually "self"
            try:
                # translate usertype string to int
                types = {"default": -1, "club": 0, "admin": 1, "dev": 2}
                # get user credentials
                actualuser = checkCredentials(args[0].DBC)
                # if user is not usertype "dev"
                if actualuser != 2:
                    # if usertype is single string
                    if type(usertype) is str:
                        # if user is not indicated usertype
                        if actualuser != types[usertype]:
                            # redirect to homepage
                            raise cherrypy.HTTPRedirect("/", 307)
                    # if usertype is list of strings
                    elif type(usertype) is list:
                        # if user is not in indicated usertypes
                        if actualuser not in [types[u] for u in usertype]:
                            # redirect to homepage
                            raise cherrypy.HTTPRedirect("/", 307)
            # if some cherrypy http error occurs
            except cherrypy.HTTPError as error:
                # display the http error
                return error
            # return wrapped function
            return func(*args, **kwargs)

        # return wrapped function
        return func_wrap

    # return wrapped function
    return wrap


# (to be used for passing user info to header.mako)
# returns None or a tuple: (ID, type)
def getUserType(DBC=None):
    # get user's request cookies
    requestCookie = cherrypy.request.cookie
    # if user has existing ID cookie
    if "orgdb.ID" in requestCookie.keys():
        # get user credentials
        type = checkCredentials(DBC)
        # if user is logged-in
        if type != -1:
            # return ID and usertype
            return requestCookie["orgdb.ID"].value, type
    # return None if user is not logged-in
    return None


# for checking the credentials of a logged-in user
# returns -1 if invalid/logged-out, type (0:Club, 1:Admin, 2:Dev) otherwise
def checkCredentials(DBC=None):
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # create database cursor
    cur = sqlcnx.cursor(buffered=True)
    # initialize usertype to -1 (not logged-in)
    type = -1
    # get user's request cookies
    requestCookie = cherrypy.request.cookie
    # if user has existing ID & Token cookies
    if "orgdb.ID" in requestCookie.keys(
    ) and "orgdb.Token" in requestCookie.keys():
        # get ID & Token cookie values
        ID = requestCookie["orgdb.ID"].value
        Token = requestCookie["orgdb.Token"].value
        # check if ID & Token are in LoginAccessTable and not expired, and get the usertype
        cur.execute(
            "SELECT LoginCredentialsTable.Type FROM "
            "(LoginAccessTable INNER JOIN LoginCredentialsTable ON LoginAccessTable.ID = LoginCredentialsTable.ID) "
            "WHERE LoginAccessTable.ID = %(ID)s AND Token = %(Token)s AND Expires > NOW()",
            {
                "ID": ID,
                "Token": Token
            })
        res = cur.fetchall()
        # if ID & Token are in LoginAccessTable and not expired
        if cur.rowcount >= 1:
            # update token expiry date to 1 hour from now
            cur.execute(
                "UPDATE LoginAccessTable SET Expires = DATE_ADD(NOW(), INTERVAL 1 HOUR) "
                "WHERE ID = %(ID)s AND Token = %(Token)s", {
                    "ID": ID,
                    "Token": Token
                })
            # create a response cookie with refreshed Max-Age to 1 hour from now
            responseCookie = cherrypy.response.cookie
            responseCookie["orgdb.ID"] = ID
            responseCookie["orgdb.ID"]["path"] = "/"
            responseCookie["orgdb.ID"]["max-age"] = 3600
            responseCookie["orgdb.ID"]["version"] = 1
            responseCookie["orgdb.ID"]["httponly"] = True
            responseCookie["orgdb.Token"] = Token
            responseCookie["orgdb.Token"]["path"] = "/"
            responseCookie["orgdb.Token"]["max-age"] = 3600
            responseCookie["orgdb.Token"]["version"] = 1
            responseCookie["orgdb.Token"]["httponly"] = True
            # set type to the fetched usertype from LoginCredentialsTable
            type = toInt(res[0][0])
    # delete any ID-Token pairs in LoginAccessTable that's already expired
    cur.execute("DELETE FROM LoginAccessTable WHERE Expires <= NOW()")
    # commit database changes
    sqlcnx.commit()
    # close database cursor
    cur.close()
    # return usertype
    return type


# for users logging in
# creates session cookie & returns True if valid, False otherwise
def login(ID, PIN, DBC=None):
    # create response cookie
    cookie = cherrypy.response.cookie
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # check if ID-Pin pair is in LoginCredentialsTable
    creds = verifyCredentials(ID, PIN, DBC)
    # if ID-Pin pair is in LoginCredentialsTable
    if creds is not None:
        # create a random 64-byte hex token
        token = urandom(64).hex()
        # create database cursor
        cur = sqlcnx.cursor(buffered=True)
        # insert new ID-Token pair in LoginAccessTable, expiring 1 hour from now
        cur.execute(
            "INSERT INTO LoginAccessTable (ID, Token, Expires) VALUES (%(ID)s, %(Token)s, DATE_ADD(NOW(), INTERVAL 1 HOUR))",
            {
                "ID": ID,
                "Token": token
            })
        # create new ID & Token cookie, expiring 1 hour from now
        cookie["orgdb.ID"] = ID
        cookie["orgdb.ID"]["path"] = "/"
        cookie["orgdb.ID"]["max-age"] = 3600
        cookie["orgdb.ID"]["version"] = 1
        cookie["orgdb.ID"]["httponly"] = True
        cookie["orgdb.Token"] = token
        cookie["orgdb.Token"]["path"] = "/"
        cookie["orgdb.Token"]["max-age"] = 3600
        cookie["orgdb.Token"]["version"] = 1
        cookie["orgdb.Token"]["httponly"] = True
        # commit changes to database
        sqlcnx.commit()
        # close database cursor
        cur.close()
        # True: user login succeeded
        return True
    # False: user login failed
    return False


# for users logging out
# deletes session cookie and session token
def logout(DBC=None):
    # create response cookie
    responseCookie = cherrypy.response.cookie
    # get user's request cookies
    requestCookie = cherrypy.request.cookie
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # create database cursor
    cur = sqlcnx.cursor(buffered=True)
    # if user has ID & Token cookies
    if "orgdb.ID" in requestCookie.keys(
    ) and "orgdb.Token" in requestCookie.keys():
        # delete ID-Token pair from LoginAccessTable
        cur.execute(
            "DELETE FROM LoginAccessTable WHERE ID = %(ID)s AND Token = %(Token)s",
            {
                "ID": requestCookie["orgdb.ID"].value,
                "Token": requestCookie["orgdb.Token"].value
            })
        # delete ID & Token cookies
        responseCookie["orgdb.ID"] = ""
        responseCookie["orgdb.Token"] = ""
        responseCookie["orgdb.ID"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        responseCookie["orgdb.Token"][
            "expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    # commit changes to database
    sqlcnx.commit()
    # close database cursor
    cur.close()


# for new users, creates entry in LoginCredentialsTable
# returns True if successfully deleted, False otherwise
def createCredentials(ID, PIN, Type, DBC=None):
    # create new 32-byte salt
    salt = urandom(32)
    PINSalt = salt.hex()
    # hash the PIN with the salt
    PINHash = pbkdf2_hmac('sha512', bytes(PIN, "utf8"), salt, 100000).hex()
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # create database cursor
    cur = sqlcnx.cursor()
    # check if ID already exists in LoginCredentialsTable
    cur.execute("SELECT ID FROM LoginCredentialsTable WHERE ID = %(ID)s",
                {"ID": ID})
    res = cur.fetchall()
    # if ID already exists in LoginCredentialsTable
    if cur.rowcount > 0:
        # log the incident
        cherrypy.log.error(
            "Warning (Login.createCredentials): Not creating duplicate credentials ("
            + ID + ")")
        # False: error occured
        return False
    # insert ID, hash, salt, & type to LoginCredentialsTable
    cur.execute(
        "INSERT INTO LoginCredentialsTable (ID, PINHash, PINSalt, Type) "
        "VALUES (%(ID)s, %(PINHash)s, %(PINSalt)s, %(Type)s)", {
            "ID": ID,
            "PINHash": PINHash,
            "PINSalt": PINSalt,
            "Type": Type
        })
    # commit changes to database
    sqlcnx.commit()
    # close database cursor
    cur.close()
    # True: created successfully
    return True


# (not used yet, to be implemented)
# deletes credentials if ID-Pin pair is valid
def deleteCredentials(ID, PIN, DBC=None):
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # create database cursor
    check = verifyCredentials(ID, PIN, DBC)
    # if verified user found
    if check is not None:
        type, hash = check
        cur = sqlcnx.cursor(buffered=True)
        # delete ID from LoginCredentialsTable
        cur.execute(
            "DELETE FROM LoginCredentialsTable "
            "WHERE ID = %(ID)s AND PINHash = %(PINHash)s", {
                "ID": ID,
                "PINHash": hash
            })
        # commit changes to database
        sqlcnx.commit()
    else:
        # log the incident
        cherrypy.log.error(
            "Warning (Login.deleteCredentials): Tried deleting credentials of unverified user ("
            + ID + ")")
        # False: an error occured
        return False
    # close databse cursor
    cur.close()
    # True: successfully deleted
    return True


# helper method, not to be used on its own
# checks if an ID-PIN pair is in LoginCredentialsTable
# returns tuple (type (0:Club, 1:Admin), hash) if it exists, None otherwise
def verifyCredentials(ID, PIN, DBC=None):
    # connect to database if not already connected
    if DBC is None:
        DBC = DBConnection()
    sqlcnx = DBC.connect()
    # create database cursor
    cur = sqlcnx.cursor(buffered=True)
    # get hash, salt, & type with ID
    cur.execute(
        "SELECT PINHash, PINSalt, Type FROM LoginCredentialsTable "
        "WHERE ID = %(ID)s", {"ID": ID})
    res = cur.fetchall()
    # if there's exactly 1 matching ID
    if cur.rowcount == 1:
        actualHash, salt, type = res[0]
        # compute hash from input PIN & fetched salt
        computedHash = pbkdf2_hmac('sha512', bytes(PIN, "utf8"),
                                   bytes.fromhex(salt), 100000).hex()
        # if fetched hash matches computed hash
        if actualHash == computedHash:
            return type, computedHash
    # if there's more than 1 matching ID (invalid)
    elif cur.rowcount > 1:
        # log the incident
        cherrypy.log.error(
            "Warning (Login.verifyCredentials): Duplicate credentials exist ("
            + ID + ")")
    return None


# class used by CherryPy for handling /login
class Login(object):
    def __init__(self, DBC=None, Renderer=None):
        if DBC is not None:
            self.DBC = DBC
        else:
            self.DBC = DBConnection()
        if Renderer is not None:
            self.renderer = Renderer
        else:
            self.renderer = ContentRenderer()

    @cherrypy.expose
    def index(self):
        # if user is logged in, redirect to homepage
        if checkCredentials(self.DBC) != -1:
            raise cherrypy.HTTPRedirect("/", 307)
        # else, display login page
        return self.renderer.render("login.mako",
                                    {'user': None})  # display summary data

    @cherrypy.expose
    def verify(self, ID=None, PIN=None):
        # if user is logged-out
        if checkCredentials(self.DBC) == -1:
            # if input credentials are valid
            if login(ID, PIN, self.DBC) is True:
                # redirect to homepage (successful login)
                raise cherrypy.HTTPRedirect("/")
            # go back to login page
            raise cherrypy.HTTPRedirect("/login")
        # redirect to homepage (already logged in)
        raise cherrypy.HTTPRedirect("/")

    def logout(self):
        logout(self.DBC)
        raise cherrypy.HTTPRedirect("/login")