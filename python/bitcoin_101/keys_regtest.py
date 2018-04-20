import bitcoin

from bitcoin_101 import bitprint

if __name__ == '__main__':
    key = bitcoin.random_key()
    bitprint('Private key:', key)
    pub_key = bitcoin.privtopub(key)
    pub_compact_key = bitcoin.privtopub(key + '01')
    bitprint('Public key:', pub_key)
    bitprint('Public compact key:', pub_compact_key)
    signature = bitcoin.ecdsa_raw_sign(b'a message', key)
    bitprint('Signature verified:', bitcoin.ecdsa_raw_verify(b'a message', signature, pub_key))
    bitprint(
        'Signature verified with compact public key:',
        bitcoin.ecdsa_raw_verify(b'a message', signature, pub_compact_key))

    bitprint('Address:', bitcoin.pubtoaddr(pub_key, magicbyte=111))
    bitprint('Address (compact):', bitcoin.pubtoaddr(pub_compact_key, magicbyte=111))
