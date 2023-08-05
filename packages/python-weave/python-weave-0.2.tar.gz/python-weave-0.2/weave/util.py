import urllib2
import logging
import base64
import json

opener = urllib2.build_opener(urllib2.HTTPHandler)

# Command-Line helper utilities
from weave.exceptions import WeaveException

def get_root_storage_url(server, version, user_id):
    return '%s/%s/%s/storage' % (server, version, user_id)

def get_root_info_url(server, version, user_id):
    return '%s/%s/%s/info' % (server, version, user_id)


def storage_http_op(method, user_id, password, url, payload=None, as_json=True,
                    if_unmodified_since=None, with_confirmation=False,
                    with_auth=True, output_format=None):

    """Generic HTTP helper function.  Sets headers and performs I/O.

    Optionally performing JSON parsing on the result.
    """
    req = urllib2.Request(url, data=payload)
    if with_auth:
        base64string = base64.encodestring('%s:%s' % (user_id, password))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)

    if if_unmodified_since is not None:
        req.add_header("X-If-Unmodified-Since", "%s" % if_unmodified_since)

    if with_confirmation:
        req.add_header("X-Confirm-Delete", "true")

    if output_format is not None:
        req.add_header("Accept", output_format)

    req.get_method = lambda: method

    try:
        logging.debug("Making %s request to %s%s" % \
                (method, url, " with auth %s" % \
                base64string if with_auth else ""))
        f = opener.open(req)
        result = f.read()
        if as_json:
            return json.loads(result)
        else:
            return result
    except urllib2.URLError, e:
        msg = ""
        try:
            msg = e.read()
        except:
            pass
        # TODO process error code
        logging.debug("Communication error: %s, %s" % (e, msg))
        error = "Unable to communicate with Weave server: %s" % e
        error += '. Url was: %s' % url
        raise WeaveException(error)

class TextFormatter(object):
    def format(self, obj):
        self.recursePrint(obj, 0)

    def recursePrint(self, obj, depth):
        pad = ' ' * depth

        if isinstance(obj, dict):
            for key, value in obj.items():
                key = key.encode('utf-8')
                if isinstance(value, basestring):
                    print "%s%s: %s" % (pad, key, value.encode('utf-8'))
                else:
                    print "%s%s:" % (pad, key)
                    self.recursePrint(value, depth+1)
        # If the object is iterable (and not a string, strings are a special case and don't have an __iter__)
        elif hasattr(obj,'__iter__'):
            for i in obj:
                if depth == 1: print "-----"
                self.recursePrint(i, depth)
        else:
            print "%s%s" % (pad, obj)


class XMLFormatter(object):
    def format(self, obj):
        pass

class JSONFormatter(object):
    def format(self, obj):
        print obj


