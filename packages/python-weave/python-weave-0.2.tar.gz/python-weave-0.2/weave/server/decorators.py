""" Bottle decorators
"""
from weave.server.bottle import response, abort, json_dumps

def validate(**vkargs):
    """Wrapper to validate inputs -- fixed from bottle"""
    def decorator(func):
        def wrapper(*args, **kargs):
            for key, value in vkargs.iteritems():
                if key not in kargs:
                    abort(403, 'Missing parameter: %s' % key)
                try:
                    kargs[key] = value(kargs[key])
                except ValueError:
                    abort(403, 'Wrong parameter format for: %s' % key)
            return func(*args, **kargs)
        return wrapper
    return decorator

def json(func):
    def _json(*args, **kwargs):
        res = func(*args, **kwargs)
        response.content_type = 'application/json'
        return json_dumps(res)
    return _json

