"""
 User management
"""
import base64
from weave.server.bottle import request, abort

class UserManagement(object):

    def __init__(self):
        self._users = {}

    def get_user_ids(self):
        return self._users.keys()

    def get_users(self):
        return self._users.items()

    def add_user(self, username, password, email=None):
        self._users[username] = password, email

    def check_user(self, username, password):
        if username not in self._users:
            return False
        return self._users[username][0] == password

user_management = UserManagement()

def authenticated(func):
    def _authenticated(*args, **kw):
        auth = request.environ.get("HTTP_AUTHORIZATION")
        if auth is None:
            # reject
            abort(401, "Sorry, access denied.")
        user, password = base64.b64decode(auth.split()[1]).split(":")
        if not user_management.check_user(user, password):
            # reject
            abort(401, "Sorry, access denied.")

        return func(*args, **kw)
    return _authenticated

def check_username(user):
    auth = request.environ.get("HTTP_AUTHORIZATION")
    if auth is None:
        abort(401, "Sorry, access denied.")
    cuser, password = base64.b64decode(auth.split()[1]).split(":")
    if user != cuser:
        abort(401, "Sorry, access denied.")
    return user

