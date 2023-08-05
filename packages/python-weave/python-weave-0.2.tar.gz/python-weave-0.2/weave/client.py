#!/usr/bin/python

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
import sys
import logging
from optparse import OptionParser
import json

from weave.util import TextFormatter, XMLFormatter, JSONFormatter
from weave.storage import WeaveStorageContext
from weave.crypto import WeaveCryptoContext

# Begin main: If you're running in library mode, none of this matters.

_CRED_ERROR = ("The '%s' option must not be used when a credential file is"
               " provided.")
_MISSING_ARG = "The required '%s' argument is missing.  Use -h for help."

def main():
    FORMATTERS = {"text": TextFormatter(), "xml": XMLFormatter(),
                  "json": JSONFormatter()}

    # process arguments
    parser = OptionParser()
    #parser.add_option("-h")
    #parser.add_option("-h", "--help", help="print a detailed help message",
    #                  action="store_true", dest="help")
    parser.add_option("-u", "--user", help="username", dest="username")
    parser.add_option("-p", "--password",
                      help="password (sent securely to server)",
                      dest="password")
    parser.add_option("-k", "--passphrase",
                      help="passphrase (used locally)", dest="passphrase")
    parser.add_option("-c", "--collection", help="collection",
                      dest="collection")
    parser.add_option("-i", "--id", help="object ID", dest="id")
    parser.add_option("-f", "--format", help=("format (default is text; options"
                                              " are text, json, xml)"),
                      default="text", dest="format")
    parser.add_option("-K", "--credentialfile",
                      help=("get username, password, and passphrase from this "
                            "credential file (as name=value lines)"),
                      dest="credentialfile")
    parser.add_option("-v", "--verbose", help="print verbose logging",
                      action="store_true", dest="verbose")
    # parser.add_option("-I", "--interactive", help="enter interactive mode", i
    #                   action="store_true", default=False, dest="interactive")
    parser.add_option("-s", "--server",
                      help=("server URL, if you aren't using "
                            "services.mozilla.com"), dest="server")

    # TODO add support for sort, modified, etc.

    options, args = parser.parse_args()
    # {'username': None, 'verbose': True, 'format': 'text',
    # 'passphrase': None, 'password': None, 'interactive': False}

    if options.credentialfile:
        if options.username:
            print _CRED_ERROR % 'username'
            sys.exit(1)
        if options.password:
            print _CRED_ERROR % 'password'
            sys.exit(1)
        if options.passphrase:
            print _CRED_ERROR % 'passphrase'
            sys.exit(1)
        try:
            credFile = open(options.credentialfile, "r")
            for line in credFile:
                if len(line) and line[0] != '#':
                    key, value = line.split('=', 1)
                    key = key.strip()
                    if key == 'username':
                        options.username = value.strip()
                    elif key == 'password':
                        options.password = value.strip()
                    elif key == 'passphrase':
                        options.passphrase = value.strip()
        except Exception, e:
            import traceback
            traceback.print_exc(e)
            print e
            sys.exit(1)

    if not options.username:
        print _MISSING_ARG % 'username'
        sys.exit(1)
    if not options.password:
        print _MISSING_ARG % 'password'
        sys.exit(1)
    if not options.passphrase:
        print _MISSING_ARG % 'passphrase'
        sys.exit(1)

    formatter = FORMATTERS[options.format]

    if options.verbose:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.ERROR)

    # Create a storage context: this will control all the sending and retrieving of
    # data from the server
    if options.server:
        root_server = options.server
    else:
        root_server="https://auth.services.mozilla.com"

    storage_context = WeaveStorageContext(options.username, options.password,
                                          root_server=root_server)

    # Create a crypto context: this will encrypt and decrypt data locally
    crypto = WeaveCryptoContext(storage_context, options.passphrase)

    # Now do what the user asked for

    if options.collection:
        if options.id:
            # Single item
            result = storage_context.get_item(options.collection, options.id)
            if len(result['payload']) > 0:
                # Empty length payload is legal: indicates a deleted item
                resultText = json.loads(result['payload'])
                resultObject = json.loads(crypto.decrypt(resultText))
                formatter.format(resultObject)
        else:
            # Collection
            result = storage_context.get_items(options.collection)
            for item in result:
                if len(item['payload']) > 0:
                    itemText = json.loads(item['payload'])
                    itemObject = json.loads(crypto.decrypt(itemText))
                    formatter.format(itemObject)
    else:
        print "No command provided: use -h for help"

if __name__ == "__main__":
    main()

