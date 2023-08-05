####################### BEGIN LICENSE BLOCK #############################
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is Weave Python Client.
#
# The Initial Developer of the Original Code is Mozilla Corporation.
# Portions created by the Initial Developer are Copyright (C) 2009 the Initial
# Developer. All Rights Reserved.
#
# Contributor(s):
#  Michael Hanson <mhanson@mozilla.com> (original author)
#
# Alternatively, the contents of this file may be used under the terms of either
# the GNU General Public License Version 2 or later (the "GPL"), or the GNU
# Lesser General Public License Version 2.1 or later (the "LGPL"), in which case
# the provisions of the GPL or the LGPL are applicable instead of those above.
# If you wish to allow use of your version of this file only under the terms of
# either the GPL or the LGPL, and not to allow others to use your version of
# this file under the terms of the MPL, indicate your decision by deleting the
# provisions above and replace them with the notice and other provisions
# required by the GPL or the LGPL. If you do not delete the provisions above, a
# recipient may use your version of this file under the terms of any one of the
# MPL, the GPL or the LGPL.
#
###################### END LICENSE BLOCK ############################
import urllib2
import base64

from weave import DEFAULT_PROTOCOL_VERSION
from weave.exceptions import WeaveException

opener = urllib2.build_opener(urllib2.HTTPHandler)

_QUOTE_FOUND = "Weave %s may not contain the quote character"

def _has_quote(value):
    return '"' in value

def create_user(server_url, user_id, password, email, secret=None,
                captcha_challenge=None, captcha_response=None,
                version=DEFAULT_PROTOCOL_VERSION):
    """Create a new user at the given server, with the given user_id, password,
    and email.

    If a secret is provided, or a captcha_challenge/captcha_response pair,
    those will be provided as well.  Note that the exact new-user-authorization
    logic is determined by the server."""

    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    if _has_quote(email):
        raise ValueError(_QUOTE_FOUND % 'email addresses')

    if secret is not None and _has_quote(secret):
        raise ValueError(_QUOTE_FOUND % 'secret')

    url = server_url + "/user/1/%s/" % user_id
    secret_str = ""
    captcha_str = ""

    if secret is not None:
        secret_str = ''', "secret":"%s"''' % secret

    if captcha_challenge and captcha_response:
        if secret is not None:
            raise WeaveException("Cannot provide both a secret and a "
                                 "captcha_response to createUser")

        captcha_str = (''', "captcha-challenge":"%s",
                       "captcha-response":"%s"''' % (captcha_challenge,
                                                     captcha_response))

    payload = '''{"password":"%s", "email": "%s"%s%s}''' % \
            (password, email, secret_str, captcha_str)

    req = urllib2.Request(url, data=payload)
    req.get_method = lambda: 'PUT'
    try:
        f = opener.open(req)
        result = f.read()
        if result != user_id:
            raise WeaveException(("Unable to create new user: got return"
                                  " value '%s' from server") % result)

    except urllib2.URLError, e:
        msg = ""
        try:
            msg = e.read()
        except:
            pass
        raise WeaveException(("Unable to communicate with "
                              "Weave server: ") + str(e) + "; %s" % msg)


def check_name_available(server_url, user_id,
                         version=DEFAULT_PROTOCOL_VERSION):
    """Returns a boolean for whether the given user_id is available at
    the given server."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    url = server_url + "/user/1/%s/" % user_id
    req = urllib2.Request(url)
    try:
        f = urllib2.urlopen(req)
        result = f.read()
        if result == "1":
            return False
        elif result == "0":
            return True
        else:
            raise WeaveException(("Unexpected return value from server "
                                "on name-availability request: '%s'") % result)
    except urllib2.URLError, e:
        raise WeaveException("Unable to communicate with Weave server: "
                             + str(e))


def get_user_storage_node(server_url, user_id, password,
                          version=DEFAULT_PROTOCOL_VERSION):
    """Returns the URL representing the storage node for the given user.

    Note that in the 1.0 server implementation hosted by Mozilla, the password
    is not actually required for this call."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    url = server_url + "/user/1/%s/node/weave" % user_id
    req = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    try:
        f = opener.open(req)
        result = f.read()
        f.close()
        return result

    except urllib2.URLError, e:
        if str(e).find("404") >= 0:
            return server_url
        else:
            raise WeaveException("Unable to communicate with Weave server: " + str(e))


def change_user_email(server_url, user_id, password, newemail,
                      version=DEFAULT_PROTOCOL_VERSION):
    """Change the email address of the given user."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    if _has_quote(newemail):
        raise ValueError(_QUOTE_FOUND % 'email addresses')

    url = server_url + "/user/1/%s/email" % user_id
    payload = newemail
    req = urllib2.Request(url, data=payload)
    base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.get_method = lambda: 'POST'
    try:
        f = opener.open(req)
        result = f.read()
        if result != newemail:
            raise WeaveException(("Unable to change user email: "
                                  "got return value '%s' from server") % result)
    except urllib2.URLError, e:
        raise WeaveException("Unable to communicate with Weave server: %s" % e)

def change_user_password(server_url, user_id, password, newpassword,
                         version=DEFAULT_PROTOCOL_VERSION):
    """Change the password of the given user."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    url = server_url + "/user/1/%s/password" % user_id
    payload = newpassword
    req = urllib2.Request(url, data=payload)
    base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.get_method = lambda: 'POST'
    try:
        f = opener.open(req)
        result = f.read()
        if result != "success":
            raise WeaveException(("Unable to change user "
                       "password: got return value '%s' from server") % result)

    except urllib2.URLError, e:
        raise WeaveException("Unable to communicate with Weave server: %s" % e)


def delete_user(server_url, user_id, password, version=DEFAULT_PROTOCOL_VERSION):
    """Delete the given user."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    url = server_url + "/user/1/%s/" % user_id
    req = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.get_method = lambda: 'DELETE'
    try:
        f = opener.open(req)
        # XXX the result here is never used
        #result = f.read()
        f.read()

    except urllib2.URLError, e:
        msg = ""
        try:
            msg = e.read()
        except:
            pass
        raise WeaveException("Unable to communicate with Weave server: " + str(e) + "; %s" % msg)


def set_user_profile(server_url, user_id, profileField, profileValue,
                     version=DEFAULT_PROTOCOL_VERSION):
    """Experimental: Set a user profile field.  Not part of the 1.0 API."""
    if _has_quote(user_id):
        raise ValueError(_QUOTE_FOUND % 'user ids')

    url = server_url + "/user/1/%s/profile" % user_id
    # XXX new password is not defined
    payload = newpassword
    req = urllib2.Request(url, data=payload)
    # XXX password is not defined
    base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
    req.add_header("Authorization", "Basic %s" % base64string)
    req.get_method = lambda: 'POST'
    try:
        f = opener.open(req)
        result = f.read()
        if result != "success":
            raise WeaveException(("Unable to change user "
                     "password: got return value '%s' from server") % result)

    except urllib2.URLError, e:
        raise WeaveException("Unable to communicate with Weave server: %s" % e)


