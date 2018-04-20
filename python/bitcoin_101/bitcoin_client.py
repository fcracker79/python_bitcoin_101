import base64
from bitcoin_101 import bitjson_dumps, bitjson_loads
import requests


class BitcoinClient:
    def __init__(self):
        btcd_auth_header = b'Basic ' + base64.b64encode(b'bitcoin:qwertyuiop')
        self.btcd_headers = {'content-type': 'application/json', 'Authorization': btcd_auth_header}

    def __getattr__(self, item):
        if item == '_call':
            return self._call
        return lambda *a, **kw: self._call(item, *a, **kw)

    def _call(self, method: str, *params, expect_json: bool=True):
        payload = bitjson_dumps({
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': 0,
        })

        resp = requests.post('http://localhost:18332', data=payload, headers=self.btcd_headers)
        content = resp.text

        if expect_json:
            content = bitjson_loads(content)
            if content['error']:
                raise ValueError('Error: {}'.format(content['error']))

            return content['result']
        return content
