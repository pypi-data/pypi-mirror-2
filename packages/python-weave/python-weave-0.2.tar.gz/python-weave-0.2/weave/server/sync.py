"""
 Sync APIs
"""
from json import loads as json_loads
from json import dumps as json_dumps

from weave.server.bottle import request, abort
from weave.server.decorators import validate, json
from weave.server.users import authenticated, check_username
from weave.server.storage import storage


class SyncServer(object):

    @validate(user_id=check_username)
    @authenticated
    @json
    def get_quota(self, user_id):
        # see the semantics of quota
        return [15, None]

    @validate(user_id=check_username)
    @authenticated
    def get_collections_timestamp(self, user_id):
        return storage.get_collections_timestamp(user_id)

    @validate(user_id=check_username)
    @authenticated
    @json
    def get_collection_counts(self, user_id):
        return storage.get_collection_counts(user_id)

    @validate(user_id=check_username)
    @authenticated
    @json
    def get_item(self, user_id, collection_id, item_id):
        item = storage.get_item(user_id, collection_id, item_id)
        # returns as json
        if item is not None:
            return json_loads(item)
        abort(404, 'Item does not exists')

    @validate(user_id=check_username)
    @authenticated
    @json
    def get_items(self, user_id, collection_id):
        return list(storage.get_items(user_id, collection_id))

    @validate(user_id=check_username)
    @authenticated
    def set_item(self, user_id, collection_id, item_id):
        # stored in pure string
        data = request.body.read()
        if not storage.set_item(user_id, collection_id, item_id, data):
            abort(500, 'Could not store %d % in %d' (item_id, collection_id))

    @validate(user_id=check_username)
    @authenticated
    def post_items(self, user_id, collection_id):
        # see how to avoid serializing/deserializing here
        data = request.body.read()
        for item in json_loads(data):
            item_id = item['id']
            item = json_dumps(item)
            storage.set_item(user_id, collection_id, item_id, item)
        # XXX need to send back the results here

    @validate(user_id=check_username)
    @authenticated
    def delete_item(self, user_id, collection_id, item_id):
        return storage.delete_item(user_id, collection_id, item_id)

    @validate(user_id=check_username)
    @authenticated
    def delete_items(self, user_id, collection_id):
        # XXX implement the ?ids=
        res = storage.delete_items(user_id, collection_id)
        if res is None:
            abort(404, 'item does not exists')

    @validate(user_id=check_username)
    @authenticated
    def delete_collection(self, user_id, collection_id):
        return storage.delete_collection(user_id, collection_id)

    @validate(user_id=check_username)
    @authenticated
    def delete_all(self, user_id):
        return storage.delete_all(user_id)

