
import urllib
import logging
import json

from weave.util import (storage_http_op, get_root_storage_url,
                        get_root_info_url)
from weave.user import get_user_storage_node
from weave import DEFAULT_PROTOCOL_VERSION


class WeaveStorageContext(object):
    """An object that encapsulates a server, userID, and password, to simplify
    storage calls for the client."""

    def __init__(self, user_id, password, root_server,
                 version=DEFAULT_PROTOCOL_VERSION):
        self.url = get_user_storage_node(root_server, user_id, password)
        if self.url[len(self.url)-1] == '/':
            self.url = self.url[:len(self.url)-1]
        self.user_id = user_id
        self.password = password
        self.version = version
        self.root_storage_url = get_root_storage_url(self.url, self.version,
                                                    self.user_id)
        self.root_info_url = get_root_info_url(self.url, self.version,
                                               self.user_id)

        logging.debug("Created WeaveStorageContext for %s: storage node is %s" \
                % (user_id, self.url))

    def _get_collection_url(self, collection, id=None, **query):
        # TODO need to use urlunparse -- much cleaner
        if len(query) > 0:
            query = urllib.urlencode(query.items())
        else:
            query = ''

        if id is None:
            url = '%s/%s' % (self.root_storage_url, collection)
        else:
            url = '%s/%s/%s' % (self.root_storage_url, collection,
                                urllib.quote(id))
        if query != '':
            return '%s?%s' % (url, query)
        return url

    def _storage_op(self, url, method, data=None, as_json=False,
                    if_unmodified_since=None,
                    with_confirmation=False, with_auth=True):
        """Wrapper to simplify http calls."""
        return storage_http_op(method, self.user_id, self.password, url,
                               data, as_json=as_json,
                               if_unmodified_since=if_unmodified_since,
                               with_confirmation=with_confirmation,
                               with_auth=with_auth)

    def http_get(self, url):
        return self._storage_op(url, "GET", as_json=True)

    #
    # Items storage APIs
    #
    def add_or_modify_item(self, collection, item, url_id=None,
                           if_unmodified_since=None):
        url = self._get_collection_url(collection)
        if url_id:
            url = '%s/%s' % (url, urllib.quote(url_id))

        if isinstance(item, str):
            item_json = item
        else:
            item_json = json.dumps(item)

        return self._storage_op(url, "PUT", item_json,
                                if_unmodified_since=if_unmodified_since)

    def add_or_modify_items(self, collection, item_array,
                            if_unmodified_since=None):
        """Adds all the items defined in 'itemArray' to 'collection'.

        Effectively performs an add_or_modifiy_item for each.

        Returns a map of successful and modified saves, like this::

          {"modified":1233702554.25,
           "success":["{GXS58IDC}12","{GXS58IDC}13","{GXS58IDC}15",
           "{GXS58IDC}16","{GXS58IDC}18","{GXS58IDC}19"],
           "failed":{"{GXS58IDC}11":["invalid parentid"],
                     "{GXS58IDC}14":["invalid parentid"],
                     "{GXS58IDC}17":["invalid parentid"],
                     "{GXS58IDC}20":["invalid parentid"]}
           }
        """
        url = self._get_collection_url(collection)
        if isinstance(item_array, str):
            item_array_json = item_array
        else:
            item_array_json = json.dumps(item_array)

        return self._storage_op(url, "POST", item_array_json,
                                if_unmodified_since=if_unmodified_since)


    def delete_item(self, collection, id, if_unmodified_since=None):
        """Deletes the item identified by collection and id."""
        url = self._get_collection_url(collection, id)
        return self._storage_op(url, "DELETE",
                                if_unmodified_since=if_unmodified_since)

    def delete_items(self, collection, id_array=None, **params):
        """Deletes the item identified by collection id_array,
        and optional parameters."""
        # TODO: Replace params with named arguments.
        if id_array is not None:
            params['ids'] = id_array
        url = self._get_collection_url(collection, **params)
        return self._storage_op(url, "DELETE", url)

    def delete_items_older_than(self, collection, timestamp):
        """Deletes all items in the given collection older than the provided
        timestamp."""
        url = self._get_collection_url(collection, timestamp=timestamp)
        return self._storage_op(url, "DELETE")

    def delete_all(self, confirm=True):
        """Deletes all items in all colletions."""
        # The only reason you'd want confirm=False is for unit testing
        return self._storage_op(self.root_storage_url, "DELETE", as_json=False,
                                with_confirmation=confirm)


    def get_collection_ids(self, collection, params=None, as_json=True,
                           output_format=None):
        """Returns collection ids"""
        url = self._get_collection_url(collection, **params)
        return self._storage_op(url, "GET", as_json=as_json,
                                 output_format=output_format)

    def get_item(self, collection, id, as_json=True, with_auth=True):
        url = self._get_collection_url(collection, id=id, full=1)
        return self._storage_op(url, "GET", as_json=as_json,
                                 with_auth=with_auth)

    def get_items(self, collection, as_json=True, with_auth=True):
        url = self._get_collection_url(collection, full=1)
        return self._storage_op(url, "GET", as_json=as_json,
                                with_auth=with_auth)


    #
    # information APIs
    #
    def _get_info(self, name):
        url= '%s/%s' % (self.root_info_url, name)
        return self._storage_op(url, "GET", as_json=True)

    def get_collection_counts(self):
        return self._get_info('collection_counts')

    def get_collection_timestamps(self):
        return self._get_info('collections')

    def get_quota(self):
        return self._get_info('quota')

