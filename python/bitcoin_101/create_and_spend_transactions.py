import typing
from pprint import pprint

import bitcoin

from bitcoin_101.bitcoin_client import BitcoinClient


def _ensure_funds(client: BitcoinClient):
    if client.call('getinfo')['balance'] < 0.1:
        client.call('generate', 106, expect_json=False)
    assert client.call('getinfo')['balance'] > 0.1


def _get_outpoints(
        client: BitcoinClient,
        btc_addresses: typing.List[str],
        btc_transactions: typing.List[str]) -> typing.Iterator[str]:
    btc_addresses = set(btc_addresses)
    for btc_transaction in btc_transactions:
        cur_tx = client.call(
            'getrawtransaction', btc_transaction, 1
        )
        for out in cur_tx['vout']:
            if out['scriptPubKey']['addresses'][0] in btc_addresses:
                yield {
                    'output': '{}:{}'.format(btc_transaction, out['n']),
                    'value': int(out['value'] * 10**8)
                }


if __name__ == '__main__':
    bitcoin_client = BitcoinClient()
    _ensure_funds(bitcoin_client)
    keys = [bitcoin.random_key() + '01' for _ in range(3)]
    pubkeys = [bitcoin.privtopub(k) for k in keys]
    addresses = [bitcoin.pubtoaddr(p, magicbyte=111) for p in pubkeys]
    an_external_address = 'mwDWoUg8vdkpDWtFY6GZJybBqNEM6mmYaz'

    print('\nPublic keys')
    pprint(pubkeys)
    print('\nAddresses')
    pprint(addresses)
    # Total: 0.06
    funding_txs = [
        bitcoin_client.call('sendtoaddress', address, 0.01 * (i + 1))
        for i, address in enumerate(addresses)
    ]
    print('\nFunding txs')
    pprint(funding_txs)
    outpoints = list(_get_outpoints(bitcoin_client, addresses, funding_txs))

    pprint(outpoints)
    tx = bitcoin.mktx(
        outpoints,
        [
            {'value': int(0.055 * 10**8), 'address': an_external_address},
            {'value': int(0.004 * 10 ** 8), 'address': addresses[0]}
        ]
    )
    print('\nUnsigned tx')
    pprint(bitcoin.deserialize(tx))
    print('\nUnsigned raw tx\n', tx)
    for i, key in enumerate(keys):
        tx = bitcoin.sign(tx, i, key)

    print('\nSigned tx')
    pprint(bitcoin.deserialize(tx))
    print('\nSigned raw tx\n', tx)
    bitcoin_client.call('sendrawtransaction', tx)
