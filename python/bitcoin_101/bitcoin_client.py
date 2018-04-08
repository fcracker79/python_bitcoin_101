import base64
import decimal
import json
import requests


class BitcoinClient(object):
    def __init__(self):
        btcd_auth_header = b'Basic ' + base64.b64encode(b'bitcoin:qwertyuiop')

        self.btcd_headers = {'content-type': 'application/json', 'Authorization': btcd_auth_header}

    def call(self, method: str, *params, expect_json: bool=True):
        payload = json.dumps({
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': 0,
        })

        resp = requests.post('http://localhost:18332', data=payload, headers=self.btcd_headers)
        content = resp.text

        if expect_json:
            content = json.loads(content, parse_float=decimal.Decimal)
            if content['error']:
                raise ValueError('Error: {}'.format(content['error']))

            return content['result']
        return content
