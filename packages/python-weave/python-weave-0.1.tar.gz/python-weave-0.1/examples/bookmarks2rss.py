""" This example script will get your bookmarks
    and build a RSS 2 feed out of them.

    It needs Mako to work.
"""
import sys
import json
import datetime
import os

from mako.template import Template
from weave.client import WeaveStorageContext, WeaveCryptoContext

_DEFAULT_SERVER = 'https://auth.services.mozilla.com'

class WeaveClient(object):

    def __init__(self, user_id, password, passphrase, server=_DEFAULT_SERVER):
        self.storage = WeaveStorageContext(user_id, password, server)
        self.crypto = WeaveCryptoContext(self.storage, passphrase)

    def _deserialize(self, payload):
        return json.loads(self.crypto.decrypt(json.loads(payload)))

    def get_bookmarks(self):
        bookmarks = [self._deserialize(item['payload'])
                     for item in self.storage.get_items('bookmarks')]

        for bookmark in bookmarks:
            bookmark = bookmark[0]
            if bookmark['type'] != 'bookmark':
                continue
            yield bookmark


now = datetime.datetime.now().isoformat()

class RSSItem(object):

    def __init__(self, bookmark):
        self.title = u'<![CDATA[%s]]>' % bookmark['title']
        self.link = u'<![CDATA[%s]]>' % bookmark['bmkUri']
        self.date = now
        self.description = u''

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(1)

    f = open(os.path.join(os.path.dirname(__file__), 'rss2.mako'))
    rss_mako = f.read()
    f.close()
    # generates a pseudo-XML stream with the bookmarks, that can be reused
    client = WeaveClient(sys.argv[1], sys.argv[2], sys.argv[3])
    items = [RSSItem(bookmark) for bookmark in client.get_bookmarks()]
    data = {'items': items, 'last_build_date': now}
    print Template(rss_mako,
                   #input_encoding='utf8',
                   output_encoding='utf-8').render(**data)

