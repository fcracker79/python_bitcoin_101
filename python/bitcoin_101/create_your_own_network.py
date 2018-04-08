from pprint import pprint

from bitcoin_101.bitcoin_client import BitcoinClient

# make start
if __name__ == '__main__':
    pprint(BitcoinClient().call('getinfo'))
    # show keys_regtest.py
