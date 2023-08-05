"""
 Database - stores the data into Redis

 *Warning* : this is not suitable for production usage
 since Redis is an in-memory database (with disk syncs).

 In Weave, every user has a list of collections, which contains items.

 + Every collection has a owner : a user
 + Every item has a owner: a collection
 + an item is a simple string

A collection has, besides a list of items, a timestamp. To store
it using redis, we can use this key:

    collection:1:f_timestamp

Where 1 is the unique ID of the collection (obtained with incr),
and f_timestamp the name of the field. the 'f_' prefix is used to
avoid any confusion with entities like collection.

Next, the best way to store relations is to use sets.

Basically, sets will let us link entities by expressing the relations
like this = SOURCE:ID:TARGET:ID

    user:1:collection 1     # user 1 has collection 1
    collection:1:user 1     # collection 1 has user 1
    collection:1:item 1     # item 1 is in collection 1
    collection:1:item 2     # item 2 is in collection 1
    item:1:collection 1     # collection 1 has item 1
    item:2:collection 1     # colection 1 has item 2

This allows us to query what items a collection has, in which
collection an item is, and so forth.

"""
import logging
from collections import defaultdict

from redis import Redis
from redis.exceptions import ConnectionError

# todo: generate timestamps
#
_REDIS = None

class _MemoryStore(object):
    """Dummy memory store.

    This is used when the redis server cannot be reached.
    """
    def __init__(self):
        self.sets = defaultdict(list)
        self.values = {}

    def sadd(self, setname, name):
        self.sets[setname].append(name)

    def sismember(self, setname, name):
        if setname not in self.sets:
            return False
        return name in self.sets[setname]

    def smembers(self, setname):
        return self.sets[setname]

    def srem(self, setname, item):
        self.sets[setname].remove(item)

    #
    # general APIs
    #
    def get(self, name):
        return self.values.get(name)

    def set(self, name, value):
        self.values[name] = value

    def delete(self, name):
        del self.values[name]

def _init_redis():
    global _REDIS
    if _REDIS is not None:
        return
    try:
        _REDIS = Redis(host='localhost', port=6379, db=0)
        _REDIS.ping()
    except ConnectionError:
        logging.warning('Redis server could not be reached. '
                        'Using memory storage')
        _REDIS = _MemoryStore()

_init_redis()

class StorageDB(dict):

    def init(self, users):
        for user_id, email in users:
            self.set_user(user_id, email)

    def _next_id(self, key):
        """Return the next id for the given key"""
        return _REDIS.incr(key)

    def _create_key(self, *args):
        return ':'.join([str(arg) for arg in args])

    #
    # Users APIs -- supposes the email is unique
    #
    def user_exists(self, email):
        """Returns user infos. user is the key"""
        return self.get_user(email) is not None

    def _email_to_id(self, email):
        user = self.get_user(email)
        return user['id']

    def set_user(self, user_id, email):
        # XXX see if we want to store other stuff than the email
        user = self.get_user(user_id)

        if user is None:
            _REDIS.sadd('users', user_id)
            user = {'email': email, 'id': user_id}
        else:
            user['email'] = email

        for field in ('email',):
            # storing the user info
            # we store the email but we will store more stuff
            key = self._create_key('user', user_id, 'f_%s' % field)
            _REDIS.set(key, user[field])

    def get_user(self, user_id):
        if not _REDIS.sismember('users', user_id):
            return None

        # return the fields (only email at this time)
        res = {}
        email_key = self._create_key('user', user_id, 'f_email')
        res['email'] = _REDIS.get(email_key)  # more info later
        return res


    #
    # Collections APIs
    #
    def _collection_set_key(self, user_id):
        return self._create_key(user_id, 'collections')

    def delete_all(self, user_id):
        set_key = self._collection_set_key(user_id)
        for collection_id in tuple(_REDIS.smembers(set_key)):
            self.delete_collection(user_id, collection_id)

    def delete_collection(self, user_id, collection_id):
        set_key = self._item_set_key(user_id, collection_id)
        for item_id in tuple(_REDIS.smembers(set_key)):
            self.delete_item(user_id, collection_id, item_id)

        set_key = self._collection_set_key(user_id)
        _REDIS.srem(set_key, collection_id)

    def collection_exists(self, user_id, label):
        """Returns user infos. user is the key"""
        set_key = self._collection_set_key(user_id)
        return _REDIS.sismember(set_key, label)

    def set_collection(self, user_id, label, count=0, timestamp=None):
        set_key = self._collection_set_key(user_id)
        if not self.collection_exists(user_id, label):
            _REDIS.sadd(set_key, label)

        # storing the collection info
        collection_key = self._create_key(user_id, label)

        _REDIS.set(self._create_key('collection', collection_key,
                                    'f_timestamp'),
                   timestamp)
        _REDIS.set(self._create_key('collection', collection_key,
                                    'f_count'), count)


    def get_collection(self, user_id, label):
        set_key = self._collection_set_key(user_id)
        if not _REDIS.sismember(set_key, label):
            return None

        # return the fields (only email at this tim)
        # XXX see how to express mappings
        collection_key = self._create_key(user_id, label)
        key = self._create_key('collection', collection_key, 'f_timestamp')
        count_key = self._create_key('collection', collection_key, 'f_count')
        return {'label': label, 'timestamp': _REDIS.get(key),
                'count': _REDIS.get(count_key)}

    def get_collections(self, user_id):
        for label in self.get_collection_ids(user_id):
            yield self.get_collection(user_id, label)

    def get_collection_ids(self, user_id):
        set_key = self._collection_set_key(user_id)
        return _REDIS.smembers(set_key)

    def get_collections_timestamp(self, user_id):
        result = {}
        for collection in self.get_collections(user_id):
            result[collection['label']] = collection['timestamp']
        return result

    def get_collection_counts(self, user_id):
        result = {}
        for collection in self.get_collections(user_id):
            result[collection['label']] = int(collection['count'])
        return result


    #
    # Items APIs
    #
    def _item_set_key(self, user_id, collection_id):
        return self._create_key(user_id, collection_id, 'items')

    def item_exists(self, user_id, collection_id, item_id):
        """Returns user infos. user is the key"""
        set_key = self._item_set_key(user_id, collection_id)
        return _REDIS.sismember(set_key, item_id)

    def get_items(self, user_id, collection_id):
        set_key = self._item_set_key(user_id, collection_id)
        for item_id in _REDIS.smembers(set_key):
            yield self.get_item(user_id, collection_id, item_id)

    def get_item(self, user_id, collection_id, item_id):
        if not self.item_exists(user_id, collection_id, item_id):
            return None
        item_key = self._create_key('item', user_id, collection_id,
                                    item_id)
        return _REDIS.get(item_key)

    def set_item(self, user_id, collection_id, item_id, data):
        set_key = self._item_set_key(user_id, collection_id)
        if not self.item_exists(user_id, collection_id, item_id):
            _REDIS.sadd(set_key, item_id)

        collection = self.get_collection(user_id, collection_id)
        if collection is None:
            count = 1
        else:
            count = int(collection['count']) + 1

        self.set_collection(user_id, collection_id, count=count)

        # storing the item info
        item_key = self._create_key('item', user_id, collection_id,
                                    item_id)
        return _REDIS.set(item_key, data)

    def delete_item(self, user_id, collection_id, item_id):

        if not self.item_exists(user_id, collection_id, item_id):
            return None

        set_key = self._item_set_key(user_id, collection_id)
        _REDIS.srem(set_key, item_id)

        item_key = self._create_key('item', user_id, collection_id,
                                    item_id)
        return _REDIS.delete(item_key)

    def delete_items(self, user_id, collection_id):
        # XXXX add options
        set_key = self._item_set_key(user_id, collection_id)
        for item_id in tuple(_REDIS.smembers(set_key)):
            self.delete_item(user_id, collection_id, item_id)
        # XXX need to return item-per-item feedback
        return True

storage = StorageDB()

