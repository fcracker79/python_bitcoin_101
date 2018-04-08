import bitcoin


def _derived_key(master_key: str, *path: int) -> str:
    k = master_key
    for p in path:
        k = bitcoin.bip32_ckd(k, p)
    return k


def _derive_and_print(master_key: str, *path: int):
    master_pub_key = _derived_key(bitcoin.bip32_privtopub(master_key))
    derived_key = _derived_key(master_key, *path)
    derived_pub_key = _derived_key(master_pub_key, *path)
    derived_pub_key_from_key = bitcoin.bip32_privtopub(derived_key)
    print(
        '''
        Master key: {}
        Derived key: {},
        Derived public key: {},
        Derived public key from private: {}
    '''.format(master_key, derived_key, derived_pub_key, derived_pub_key_from_key))


if __name__ == '__main__':
    seed = bitcoin.mnemonic_to_seed(b'This is a very funny mnemonic')
    master_key = bitcoin.bip32_master_key(seed)
    print('Master key:', master_key)
    _derive_and_print(master_key, 1, 2, 3)
    _derive_and_print(master_key, 1 + 2**31, 2, 3)