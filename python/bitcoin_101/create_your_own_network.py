from pprint import pprint

from bitcoin_101 import bitprint
from bitcoin_101.bitcoin_client import BitcoinClient

# make start
if __name__ == '__main__':
    bitprint(BitcoinClient().getinfo())
    # show keys_regtest.py
