""" Weave Storage micro-implementation.

    For testing purposes only, incomplete !!!

"""
from wsgiref.simple_server import make_server

from weave.server.bottle import Bottle, debug, yieldroutes
from weave.server.sync import SyncServer
from weave.server.users import user_management
from weave.server.storage import storage

DEFAULT_PORT = 8000

routes = {'/1.0/:user_id/info/quota': ('get_quota',),
          '/1.0/:user_id/info/collections': ('get_collections_timestamp',),
          '/1.0/:user_id/info/collection_counts': ('get_collection_counts',),
          '/1.0/:user_id/storage': (('delete_all', 'DELETE'),),
          '/1.0/:user_id/storage/:collection_id/:item_id':
                 ('get_item', ('set_item', 'PUT'), ('delete_item', 'DELETE')),
          '/1.0/:user_id/storage/:collection_id':
                 ('get_items', ('delete_items', 'DELETE'),
                  ('post_items', 'POST'))

          }


class WeaveApp(Bottle):

    def __init__(self):
        super(WeaveApp, self).__init__()
        # sync APIs
        self.sync_server = SyncServer()
        for url, handlers in routes.items():
            for handler in handlers:
                if isinstance(handler, str):
                    method = 'GET'
                else:
                    handler, method = handler
                self.add_route(getattr(self.sync_server, handler),
                               url, method=method)

    def add_route(self, callback, path=None, method='GET', **kargs):
        if isinstance(method, str): #TODO: Test this
            method = method.split(';')
        paths = [] if path is None else [path.strip().lstrip('/')]
        if not paths: # Lets generate the path automatically.
            paths = yieldroutes(callback)
        for p in paths:
            for m in method:
                route = m.upper() + ';' + p
                self.routes.add(route, callback, **kargs)

def main():
    app = WeaveApp()
    user_management.add_user('dummy', 'dummy', 'dummy@example.com')
    storage.init(user_management.get_users())
    httpd = make_server('', DEFAULT_PORT, app)
    httpd.serve_forever()

if __name__ == '__main__':
    print 'Starting Weave server at port %d' % DEFAULT_PORT
    debug(True)
    main()

