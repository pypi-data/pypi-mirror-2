import unittest2
import threading
import time
from wsgiref.simple_server import make_server

from weave.server.bottle import debug
from weave.server import WeaveApp
from weave.server.users import user_management
from weave.server.storage import storage

DEFAULT_PORT = 8000

class AppRunner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        debug(True)
        self.app = WeaveApp()
        user_management.add_user('dummy', 'dummy', 'dummy@example.com')

        for uid, (email, _) in user_management.get_users():
            storage.set_user(uid, email)
        self.httpd = make_server('', DEFAULT_PORT, self.app)

    def run(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        self.join()
        time.sleep(0.2)

