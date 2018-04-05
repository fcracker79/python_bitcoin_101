import bitcoin


if __name__ == '__main__':
    key = bitcoin.random_key()
    print('Private key:', key)
    pub_key = bitcoin.privtopub(key)
    pub_compact_key = bitcoin.privtopub(key + '01')
    print('Public key:', pub_key)
    print('Public compact key:', pub_compact_key)
    signature = bitcoin.ecdsa_raw_sign(b'a message', key)
    print('Signature verified:', bitcoin.ecdsa_raw_verify(b'a message', signature, pub_key))
    print(
        'Signature verified with compact public key:',
        bitcoin.ecdsa_raw_verify(b'a message', signature, pub_compact_key))
