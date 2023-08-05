import restkit
import hashlib
try:
    import json
except ImportError, e:
    import simplejson as json

from uuid import uuid4
from time import time as unix_time
from urllib import urlencode

import logging
logging.basicConfig(filename='client_log.txt', level=logging.DEBUG)

__all__ = ["Client"]

class Client(object):
    """Requires `app_secret` and `app_key` as supplied by BigDoor.
    Optional `api_host` parameter allows for use with API compatible
    services and/or staging servers.
    """
    def __init__(self, app_secret, app_key, api_host=None):
        """Constructor for a `Client` object.

        more docs here please
        """
        self.app_secret = app_secret
        self.app_key = app_key
        if not api_host:
            api_host = "http://api.bigdoor.com"
        self.api_host = api_host
        self.base_url = "/api/publisher/%s" % self.app_key
        self.conn = restkit.Resource(self.api_host)

    def generate_token(self):
        return uuid4().hex

    def generate_signature(self, url, params=None, payload=None):
        """Generates the appropriate signature given a url and optional
        params."""
        sig = url
        if params:
            sig += self._flatten_params(params)
        if payload:
            sig += self._flatten_params(payload)
        sig += self.app_secret
        return hashlib.sha256(sig).hexdigest()

    def _flatten_params(self, params):
        """Flattens a parameter dictionary for signature generation"""
        keys = params.keys()
        keys.sort()
        return "".join(["%s%s" % (k, params[k]) for k in keys if k not in ('sig', 'format')])

    def _sign_request(self, method, url, params=None, payload=None):
        if params is None:
            params = {}
        is_postish = method in ['post', 'put']

        # The payload time is assumed to be the correct value
        if is_postish and 'time' in payload:
            params['time'] = payload['time']
        if not 'time' in params:
            params['time'] = str(unix_time())
        if is_postish and not 'time' in payload:
            payload['time'] = params['time']

        if is_postish and not 'token' in payload:
            payload['token'] = self.generate_token()

        params['sig'] = self.generate_signature(url, params, payload)
        return params, payload

    def _abs_from_rel(self, url):
        return "%s/%s" % (self.base_url, url)

    def do_request(self, method, endpoint, params=None, payload=None):
        method = method.lower()
        url = self._abs_from_rel(endpoint)
        params, payload = self._sign_request(method, url, params, payload)
        func = getattr(self.conn, method)
        if method in ['post', 'put']:
            params['payload'] = payload
        return func(url, **params)

    def get(self, endpoint, params=None):
        r = self.do_request('get', endpoint, params)
        return json.loads(r.body)

    def delete(self, endpoint, params=None):
        r = self.do_request('delete', endpoint, params)
        return json.loads(r.body)

    def post(self, endpoint, params=None, payload=None):
        r = self.do_request('post', endpoint, params, payload)
        return json.loads(r.body)

    def put(self, endpoint, params=None, payload=None):
        r = self.do_request('put', endpoint, params, payload)
        return json.loads(r.body)
