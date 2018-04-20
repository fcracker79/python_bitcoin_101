import bitcoin

from bitcoin_101 import bitprint

if __name__ == '__main__':
    key = bitcoin.random_key()

    outpoints = {
        '97f7c7d8ac85e40c255f8a763b6cd9a68f3a94d2e93e8bfa08f977b92e55465e:0': 50000,
        '4cc806bb04f730c445c60b3e0f4f44b54769a1c196ca37d8d4002135e4abd171:1': 50000
    }

    tx = bitcoin.mktx(
        [{'output': k, 'value': v} for k, v in outpoints.items()],
        [{'value': 90000, 'address': '16iw1MQ1sy1DtRPYw3ao1bCamoyBJtRB4t'}]
    )
    bitprint('Raw transaction:', tx)
    bitprint('Deserialized transaction')
    bitprint(bitcoin.deserialize(tx))

    one_signed_tx = bitcoin.sign(tx, 0, key)
    bitprint(one_signed_tx)
    bitprint('ScriptSig for the first input')
    bitprint(bitcoin.deserialize_script(
        bitcoin.deserialize(one_signed_tx)['ins'][0]['script'])
    )
    bitprint('ScriptPubKey for the first output')
    bitprint(bitcoin.deserialize_script(
        bitcoin.deserialize(one_signed_tx)['outs'][0]['script'])
    )
