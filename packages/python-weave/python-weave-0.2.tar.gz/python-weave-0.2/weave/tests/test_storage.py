import unittest2
import socket

from weave.tests.support import AppRunner, DEFAULT_PORT
from weave.storage import WeaveStorageContext
from weave.crypto import WeaveCryptoContext

_SERVER = 'http://127.0.0.1'

class TestStorage(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = AppRunner()
        cls.app.start()
        user_id = 'dummy'
        password = 'dummy'
        passphrase = 'dummy'
        server = '%s:%d' % (_SERVER, DEFAULT_PORT)
        cls.storage = WeaveStorageContext(user_id, password, server)
        cls.crypto = WeaveCryptoContext(cls.storage, passphrase)

    @classmethod
    def tearDownClass(cls):
        cls.app.stop()

    def test_dummy(self):
        # just to make sure the server is up and running
        # this should not raise an error
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', DEFAULT_PORT))
        s.send('BLABLABLABLA')
        s.close()

    def test_get_quota(self):
        quota = self.storage.get_quota()
        self.assertEquals(quota, [15, None])

    def test_collections(self):
        self.storage.delete_all()

        data = {'item1': 1}
        self.storage.add_or_modify_item('bookmark', data, '1')
        res = self.storage.get_item('bookmark', '1')
        self.assertEquals(res, data)

        count = self.storage.get_collection_counts()
        self.assertEquals(count, {u'bookmark': 1})

        self.storage.add_or_modify_item('bookmark', 'data2', '2')
        count = self.storage.get_collection_counts()
        self.assertEquals(count, {u'bookmark': 2})

        res = self.storage.get_items('bookmark')
        self.assertEquals(res, [u'{"item1": 1}', u'data2'])

        # try to delete a collection
        self.storage.delete_items('bookmark')
        res = self.storage.get_items('bookmark')
        self.assertEquals(res, [])

