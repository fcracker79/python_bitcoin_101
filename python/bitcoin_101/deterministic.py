import bitcoin
from hashlib import pbkdf2_hmac


def _mnemonic_to_seed(mnemonic_phrase, passphrase=b''):
    return pbkdf2_hmac(hash_name='sha512', password=mnemonic_phrase, salt=b'mnemonic' + passphrase, iterations=2048)


def _derived_key(master_key: str, *path: int) -> str:
    k = master_key
    for p in path:
        k = bitcoin.bip32_ckd(k, p)
    return k


def _derive_and_print(master_key: str, *path: int, derive_pub_key: bool=True):
    master_pub_key = _derived_key(bitcoin.bip32_privtopub(master_key))
    derived_key = _derived_key(master_key, *path)
    if derive_pub_key:
        derived_pub_key = _derived_key(master_pub_key, *path)
    else:
        derived_pub_key = 'N.A.'
    derived_pub_key_from_key = bitcoin.bip32_privtopub(derived_key)
    print(
        '''    Derivation path: ({}),
    Derived key: {},
    Derived public key: {},
    Derived public key from private: {}
    '''
        .format(
            ', '.join(str(x) if x <= 2 ** 31 else str(x - 2 ** 31) + '\'' for x in path),
            master_key,
            derived_key, derived_pub_key, derived_pub_key_from_key))


def _print_master_key_and_derived(vbytes: bytes):
    seed = _mnemonic_to_seed(b'This is a very funny mnemonic')
    master_key = bitcoin.bip32_master_key(seed, vbytes=vbytes)
    print('Master key:', master_key)
    _derive_and_print(master_key, 1, 2, 3)
    _derive_and_print(master_key, 1 + 2 ** 31, 2, 3, derive_pub_key=False)


if __name__ == '__main__':
    print('\nMAINNET\n')
    _print_master_key_and_derived(bitcoin.MAINNET_PRIVATE)
    print('\nTESTNET\n')
    _print_master_key_and_derived(bitcoin.TESTNET_PRIVATE)
