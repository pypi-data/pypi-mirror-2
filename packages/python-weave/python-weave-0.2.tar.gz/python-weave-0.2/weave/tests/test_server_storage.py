import unittest2

from weave.server.storage import StorageDB

class StorageDBTestCase(unittest2.TestCase):

    def test_users(self):
        db = StorageDB()
        db.set_user('tarek', 'tarek@ziade.org')
        res = db.get_user('tarek')
        self.assertEquals(res['email'], 'tarek@ziade.org')
        self.assert_(db.user_exists('tarek'))

    def test_collections(self):

        db = StorageDB()
        db.init([('tarek', 'tarek@ziade.org')])
        db.set_collection('tarek', 'bookmarks')
        db.collection_exists('tarek', 'bookmarks')

        c = db.get_collection('tarek', 'bookmarks')
        self.assertEquals(c['label'], 'bookmarks')

        ids = db.get_collection_ids('tarek')
        self.assertEquals(len(ids), 1)

        stamps = db.get_collections_timestamp('tarek')
        self.assertIn('bookmarks', stamps)

    def test_items(self):
        db = StorageDB()
        db.init([('tarek', 'tarek@ziade.org')])
        db.set_item('tarek', 'bookmarks', '1', 'blbablalba')
        res = db.get_item('tarek', 'bookmarks', '1')
        self.assertEquals(res, 'blbablalba')

        res = db.delete_item('tarek', 'bookmarks', '1')
        self.assert_(not db.item_exists('tarek', 'bookmarks', '1'))

    def test_delete_collections(self):
        db = StorageDB()
        db.init([('tarek', 'tarek@ziade.org')])
        db.set_item('tarek', 'bookmarks', '1', 'blbablalba')
        db.set_item('tarek', 'bookmarks', '2', 'blbablalba')
        self.assert_(db.collection_exists('tarek', 'bookmarks'))
        db.set_item('tarek', 'bookmarks2', '3', 'blbablalba')
        self.assert_(db.collection_exists('tarek', 'bookmarks2'))

        db.delete_collection('tarek', 'bookmarks')
        self.assert_(not db.collection_exists('tarek', 'bookmarks'))
        self.assert_(not db.item_exists('tarek', 'bookmarks', '1'))
        self.assert_(not db.item_exists('tarek', 'bookmarks', '2'))
        self.assert_(db.item_exists('tarek', 'bookmarks2', '3'))

        db.delete_all('tarek')
        self.assert_(not db.collection_exists('tarek', 'bookmarks2'))
        self.assert_(not db.item_exists('tarek', 'bookmarks2', '3'))


    def test_load(self):

        db = StorageDB()
        for i in range(1000):
            if i == 500:
                db.set_user('tarek', 'tarek@ziade.org')
            db.set_user(str(i), 'tarek@ziade.org')
        self.assert_(db.user_exists('tarek'))


