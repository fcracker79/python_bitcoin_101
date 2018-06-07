import typing

import bitcoin

from bitcoin_101 import bitprint
from bitcoin_101.bitcoin_client import BitcoinClient


def _ensure_funds(client: BitcoinClient):
    if client.getinfo()['balance'] < 0.1:
        client.generate(106, expect_json=False)
    assert client.getinfo()['balance'] > 0.1


def _get_outpoints(
        client: BitcoinClient,
        btc_addresses: typing.List[str],
        btc_transactions: typing.List[str]) -> typing.Iterator[str]:
    btc_addresses = set(btc_addresses)
    for btc_transaction in btc_transactions:
        cur_tx = client.getrawtransaction(btc_transaction, 1)
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

    bitprint('\nPublic keys\n', pubkeys)
    bitprint('\nAddresses\n', addresses)
    # Total: 0.06
    funding_txs = [
        bitcoin_client.sendtoaddress(address, 0.01 * (i + 1))
        for i, address in enumerate(addresses)
    ]
    bitprint('\nFunding txs')
    bitprint(funding_txs)
    outpoints = list(_get_outpoints(bitcoin_client, addresses, funding_txs))

    bitprint(outpoints)
    tx = bitcoin.mktx(
        outpoints,
        [
            {'value': int(0.055 * 10**8), 'address': an_external_address},
            {'value': int(0.004 * 10 ** 8), 'address': addresses[0]}
        ]
    )
    bitprint('\nUnsigned tx')
    bitprint(bitcoin.deserialize(tx))
    bitprint('\nUnsigned raw tx\n', tx)
    for i, key in enumerate(keys):
        tx = bitcoin.sign(tx, i, key)

    bitprint('\nSigned tx')
    bitprint(bitcoin.deserialize(tx))
    bitprint('\nSigned raw tx\n', tx)
    bitprint('\nHash of submitted transaction:', bitcoin_client.sendrawtransaction(tx))
    bitprint('\nMempool:', bitcoin_client.getrawmempool())
    block_hash = bitcoin_client.generate(1)[0]
    block = bitcoin_client.getblock(block_hash)
    bitprint('\nBlock that included transaction:\n', block)

